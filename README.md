# BEWARE THAT THESE INSTRUCTIONS ARE INCOMPLETE, BROKEN -- DO NOT WORK!!!


# zabbix-urbackup
How to monitor urbackup clients with zabbix.

Code from a [Zabbix forum](https://www.zabbix.com/forum/zabbix-help/409665-newbie-monitoring-urbackup) post by [tmueko](https://www.zabbix.com/forum/member/316499-tmueko)

# Step 1
On your zabbix machine install python and the [urbackup python API](https://github.com/uroni/urbackup-server-python-web-api-wrapper).
```
pip3 install urbackup-server-web-api-wrapper
cd /usr/lib/zabbix/externalscripts/
git clone git@github.com:kerryland/zabbix-urbackup.git
chmod +x  /usr/lib/zabbix/externalscripts/zabbix-urbackup/urbackup-discovery.py
```
# Step 2
Tell Zabbix how to call the urbackup api script.
- `echo UserParameter=urbackup.discovery[*],/usr/lib/zabbix/externalscripts/zabbix-urbackup/urbackup-discovery.py $1 $2 $3 >> /etc/zabbix/zabbix_agentd.conf`
# Step 3
In Zabbix, create an "Item" of type "[External Check](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/external)" against the urbackup client with a "Key" like this:
`zabbix-urbackup/urbackup-discovery.py
eg: `UserParameter=mysql.ping,mysqladmin -uroot ping | grep -c alive`
* An [External Check](https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/external), eg: `check_oracle.sh["-h","{HOST.CONN}"]`
