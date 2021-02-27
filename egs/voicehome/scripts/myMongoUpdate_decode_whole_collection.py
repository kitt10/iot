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

with open('mongo_query_output_undecoded.txt', 'w') as f:
    for x in mydoc:
        # print(x)
        f.write("%s\n" % x['_id'])

mydoc1 = mycol.find()
with open('mongo_update_undecoded.txt', 'w') as f:
    for res in mydoc1:
        try:
            res_dec = res["payload"].decode("utf8")
        except:
            continue
        res_json = json.loads(res_dec)

        res["payload"] = json.dumps(res_json)

        myquery = {"_id": res['_id']}
        newvalues = {"$set": {
            "payload": json.dumps(res_json)
        }
        }
        x = mycol.update(myquery, newvalues)
        print(res['_id'], " data updated.")
        print('newvalues =', newvalues)
