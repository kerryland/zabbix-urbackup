# BEWARE THAT THESE INSTRUCTIONS ARE INCOMPLETE, BROKEN -- DO NOT WORK!!!


# zabbix-urbackup
How to monitor UrBackup clients with Zabbix.

This code originally came from a [Zabbix forum](https://www.zabbix.com/forum/zabbix-help/409665-newbie-monitoring-urbackup) post by [tmueko](https://www.zabbix.com/forum/member/316499-tmueko)

# Step 1. Install some bits
1. Install a Zabbix Agent on your UrBackup server, if it's not there already
2. Install a Python on your UrBackup server, if it's not there already
3. Install this code on your UrBackup server
```
cd /opt
git clone git@github.com:kerryland/zabbix-urbackup.git
chmod +x  /opt/zabbix-urbackup/urbackup-discovery.py
```
# Step 2. Tell Zabbix Agent about the script
1. Add a "User Parameter" to the Zabbix Agent on the UrBackup server:
`echo 'UserParameter=urbackup.discovery[*],/opt/zabbix-urbackup/urbackup-discovery.py $1 $2 $3' >> /etc/zabbix/zabbix_agentd.conf`
2. Test it with `zabbix_agentd -t urbackup.discovery`. It will fail as shown below -- that's OK:
```
urbackup.discovery                            [t|Traceback (most recent call last):
  File "/opt/zabbix-urbackup/urbackup-discovery.py", line 14, in <module>
    server = urbackup_api.urbackup_server(sys.argv[1],sys.argv[2],sys.argv[3])
IndexError: list index out of range]
```
3. Tell the Zabbix Server about it: `zabbix_agentd -R userparameter_reload`

# Step 3. Configure Zabbix Server
1. Import the template configuration.
   - Menu: `Configuration | Templates`
   - `Import` button in top-right corner
   - Select the `Urbackup.yaml` file you downloaded earlier
  
# Step 4. Configure the UrBackup host in Zabbix
2. Find your UrBackup server in Zabbix UI (Menu: `Configuration | Hosts`), and add the "Urbackup" template to the host, add click "Update".
3. Click "Test" and configure the "Macros" fields with your Urbackup server URL, username and password. Note the URL ends in `/x` for some obscure reason. eg: `http://127.0.0.1:55414/x`
4. Click "Get value and test", which should result in a "result" looking something like this: `[{"client_version_string": "2.5.21", "delete_pending": "", "file_ok": true...`
5. Click "Update" again to save these changes to the Host's Item.
6. Define Macros for the host.
    - Click "Macros"
    - Click "Inherited and host macros"
    - Change the values for `{$UR_PASSWORD}`, `{$UR_URL}` and `{$UR_USER}` to match your environment
7. Edit the "Urbackup: urbackup discovery item" associated with your UrBackup host.
   - This requires clicking 3 dots and selecting "Item" from the menu.
   - Click "Preprocessing"
   - Click "Clone" (no idea why, but you can't add any preprocessing steps otherwise)
   - Click "Add" link (not the "Add" button)
   - Define a "Name" of "JSONPath" and a "Parameters" of (something like: `$[?(@.lastseen < 1700000000)]..lastbackup` )

