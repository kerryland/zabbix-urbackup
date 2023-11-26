# zabbix-urbackup
How to monitor [UrBackup](https://www.urbackup.org/) clients with [Zabbix](https://www.zabbix.com/).

This code originally came from a [Zabbix forum](https://www.zabbix.com/forum/zabbix-help/409665-newbie-monitoring-urbackup) post by [tmueko](https://www.zabbix.com/forum/member/316499-tmueko), plus a copy of the [urbackup api by uroni](https://github.com/uroni/urbackup-server-python-web-api-wrapper).

These instructions are my fault -- please let me know if I've got something wrong. I am a million miles away from being an experienced Zabbix user and found installation process "quirky", hence this document. I do note that Zabbix 6.4 has definite usability improvements over 6.2, so well done to you folks.

# Step 1. Install some bits
1. Install a Zabbix Agent on your UrBackup server, if it's not there already (which would surprise me!)
1. Install a Python on your UrBackup server, if it's not there already
1. Install [this code](https://github.com/kerryland/zabbix-urbackup/releases/), into `/opt`, on your UrBackup server, or grab it via git
```
cd /opt
git clone git@github.com:kerryland/zabbix-urbackup.git
chmod +x  /opt/zabbix-urbackup/urbackup-discovery.py
```

# Step 2. Tell Zabbix Agent about the script
1. Add a "User Parameter" to the Zabbix Agent on the UrBackup server:
`echo 'UserParameter=urbackup.discovery[*],/opt/zabbix-urbackup/urbackup-discovery.py $1 $2 $3' >> /etc/zabbix/zabbix_agentd.conf`
1. Test it with `zabbix_agentd -t urbackup.discovery`. It's OK if it fails as shown below:
```
urbackup.discovery                            [t|Traceback (most recent call last):
  File "/opt/zabbix-urbackup/urbackup-discovery.py", line 14, in <module>
    server = urbackup_api.urbackup_server(sys.argv[1],sys.argv[2],sys.argv[3])
IndexError: list index out of range]
```
3. Tell the Zabbix Server about it: `zabbix_agentd -R userparameter_reload`

# Step 3. Configure Zabbix Server
1. Import the template configuration.
   - Menu: `Data collection | Templates`
   - `Import` button in top-right corner
   - Select the `Urbackup.yaml` file you downloaded earlier
  
# Step 4. Configure the UrBackup host in Zabbix
1. Find your UrBackup server in Zabbix UI (Menu: `Data collection | Hosts`), and add the "Urbackup" template to the host, add click "Update".
1. Notice you now have a "urbackup discovery item" added to your host's list of items. Click on it to view the details.
1. Click "Test" and configure the "Macros" fields with your Urbackup server URL, username and password. Note the URL ends in `/x` for some obscure reason. eg: `http://127.0.0.1:55414/x`
1. Click "Get value and test", which should result in a "result" looking something like this: `[{"client_version_string": "2.5.21", "delete_pending": "", "file_ok": true...`.
1. Click "Cancel" to close the test dialog
1. Define Macros for the host.
    - Open the "Host" definition again and Click "Macros" at the top of the screen
    - Click "Inherited and host macros"
    - Change the values for `{$UR_PASSWORD}`, `{$UR_URL}` and `{$UR_USER}` to match your environment
1. Create the new automated urbackup items
   - Open the "Host" definition again and Click "Discovery rules" at the top of the screen
   - Click "urbackup discovery" (not "urbackup discovery item")
   - Click "Execute now"

TADA! You should now have a whole pile of items and triggers defined for your urbackup clients.


