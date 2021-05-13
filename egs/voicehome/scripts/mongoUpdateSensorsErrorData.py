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

mydoc1 = mycol.find()
with open('mongo_update_changed.txt', 'w') as f1:
    with open('mongo_update_wrong_status.txt', 'w') as f:
        for res in mydoc1:
            changed = False
            res_dec = res["payload"]
            res_json = json.loads(res_dec)

            if "status" in res_json:
                res_json["state"] = res_json["status"]
                del res_json["status"]
                f.write("status %s\n" % res['_id'])
                changed = True

            if "humidity_value" in res_json:
                if res_json["humidity_value"] <= 0 or res_json["humidity_value"] > 100:
                    res_json['status'] = 'error'
                    f.write("humidity_value %s\n" % res['_id'])
                    changed = True

            if "temperature_value" in res_json:
                if res_json["temperature_value"] < -55 or res_json["temperature_value"] > 125:
                    res_json['status'] = 'error'
                    f.write("temperature_value %s\n" % res['_id'])
                    changed = True

            if "pressure_value" in res_json:
                if res_json["pressure_value"] < 300 or res_json["pressure_value"] > 1100:
                    res_json['status'] = 'error'
                    f.write("pressure_value %s\n" % res['_id'])
                    changed = True

            if changed:
                res["payload"] = json.dumps(res_json)

                myquery = {"_id": res['_id']}
                newvalues = {"$set": {
                    "payload": json.dumps(res_json)
                    }
                }
                x = mycol.update(myquery, newvalues)
                print(res['_id'], " data updated.")
                print('newvalues ', newvalues)
