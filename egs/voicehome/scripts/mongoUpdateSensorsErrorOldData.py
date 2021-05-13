import pymongo
import json
import datetime
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
with open('mongo_update_wrong_date.txt', 'w') as f:
    with open('mongo_update_wrong_date_exception.txt', 'w') as f_exception:
        for res in mydoc1:
            res_dec = res["payload"]
            # res_dec = res["payload"].decode("utf8")
            res_json = json.loads(res_dec)

            if 'timestamp' in res_json:
                try:
                    date_time_obj = datetime.datetime.strptime(res_json['timestamp'], '%Y-%m-%d %H:%M:%S')


                except:
                    f_exception.write("%s\n" % res_json['timestamp'])
                    print("exception!!!")
                    continue

                if date_time_obj.year <= 2019:
                    f.write("%s\n" % json.dumps(res_json))
                    res_json['state'] = 'error'


                    myquery = {"_id": res['_id']}
                    newvalues = {"$set": {
                        "payload": json.dumps(res_json)
                    }
                    }
                    x = mycol.update(myquery, newvalues)
                    print(res['_id'], " data updated.")
                    print('newvalues ', newvalues)

