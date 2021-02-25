from datetime import datetime

res_i = {"location": "room_1", "owner": "jsanda", "status": "ok", "sensor_id": "ds18b20_1", "quantity": "degrees", "timestamp": "2021-02-25 12:44:31", "temperature_value": 18.3125}
maxLoc = 2
loc = res_i['location']
loc =int(loc.replace('room_',''))

ls= []
ls.append(res_i['timestamp'].replace('-','/') + loc*',' + str(res_i['temperature_value']) + (maxLoc-loc)*','+'\n')


print('comp')