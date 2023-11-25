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
2. Find your UrBackup server in Zabbix UI (Menu: `Configuration | Hosts`), and click "Items", then "Create Item" (button top right). [ref. official docs](https://www.zabbix.com/documentation/current/en/manual/config/items/item)
  - **Name:** urbackup discovery item
  - **Key:** urbackup.discovery[{$UR_URL},{$UR_USER},{$UR_PASSWORD}]
  - **Update Interval:** 4h
  - Test the configuration with properties appropriate for your urbackup server. Note the URL ends in `/x` for some obscure reason. eg: http://192.168.1.25:55414/x
    


In Zabbix, create an "Item" of type "[External Check](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/external)" against the UrBackup Server with a "Key" like this:
`zabbix-urbackup/urbackup-discovery.py
eg: `UserParameter=mysql.ping,mysqladmin -uroot ping | grep -c alive`
* An [External Check](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/external), eg: `check_oracle.sh["-h","{HOST.CONN}"]`
