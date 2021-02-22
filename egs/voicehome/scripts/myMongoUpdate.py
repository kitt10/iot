import pymongo
import json
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

# find by topic
# myquery = { "key": "voicehome/sensors/temperature" }
# find by id
# myquery = { "_id": ObjectId('600b66a74b673e62da5d999f') }


mydoc = mycol.find()

with open('mongo_query_output.txt', 'w') as f:
    for x in mydoc:
      # print(x)
      f.write("%s\n" % x['_id'])

with open('mongo_update_wrong_status.txt', 'w') as f:
    for res in mydoc:
        res_dec = res["payload"].decode("utf8")
        res_json = json.loads(res_dec)

        if res_json['location'] == 'room1':
            res_json['sensor_id'] = 'bme280_1'
            # res_json.pop('status')
            if "humidity_value" in res_json:
                if res_json["humidity_value"] <= 0 or res_json["humidity_value"]>100:
                    res_json['status'] = 'error'
                    f.write("%s\n" % res['_id'])
            if "temperature_value" in res_json:
                if res_json["temperature_value"] < -40 or res_json["temperature_value"]>85:
                    res_json['status'] = 'error'
                    f.write("%s\n" % res['_id'])
            if "pressure_value" in res_json:
                if res_json["pressure_value"] < 300 or res_json["pressure_value"]>1100:
                    res_json['status'] = 'error'
                    f.write("%s\n" % res['_id'])


        if res_json['location'] == 'room2':
            res_json['sensor_id'] = 'ds18b20_1'
            if "temperature_value" in res_json:
                if res_json["temperature_value"] < -55 or res_json["temperature_value"] >125:
                    res_json['status'] = 'error'
                    f.write("%s\n" % res['_id'])
        res["payload"] = json.dumps(res_json)

        myquery = {"_id": res['_id']}
        newvalues = {"$set": {
            "payload": json.dumps(res_json)
            }
        }
        x = mycol.update(myquery, newvalues)
        print(res['_id'], " data updated.")
