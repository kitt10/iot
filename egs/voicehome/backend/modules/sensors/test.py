from datetime import datetime
import re

res_i = {"location": "room_1", "owner": "jsanda", "status": "ok", "sensor_id": "ds18b20_1", "quantity": "degrees", "timestamp": "2021-02-25 12:44:31", "temperature_value": 18.3125}
maxLoc = 2
loc = res_i['location']
loc =int(loc.replace('room_',''))

ls= []
ls.append(res_i['timestamp'].replace('-','/') + loc*',' + str(res_i['temperature_value']) + (maxLoc-loc)*','+'\n')


string = 'dsroom_1234'
pattern = re.compile("^(room_)(\d)+$")
print(pattern.match(string))
omg = pattern.match(string)
if pattern.match(string):
    print('match')
else:
    print("nomatch")

print('comp')