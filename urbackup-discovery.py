#!/usr/bin/python3
#!/usr/bin/env python3

import urbackup_api
import json
import sys
import ssl
# Отключить проверку сертификатов при подключении по HTTPS (иначе если сертификат самоподписанный, подключения не будет, определено скорее всего где-то в ssl.py)
ssl._create_default_https_context = ssl._create_unverified_context
# Короткий тест подключения к серверу, логин и пароль поменять на свои
#server = urbackup_api.urbackup_server("http://10.10.10.127:55414/x", "admin", "pasword")
#for client in server.get_status():
#    print(client)
server = urbackup_api.urbackup_server(sys.argv[1],sys.argv[2],sys.argv[3])
i = 0
print ("[", end='')
for client in server.get_status():
    if i > 0 : print("," , end='')
    print(json.dumps(client))
    i += 1
print ("]", end='')
