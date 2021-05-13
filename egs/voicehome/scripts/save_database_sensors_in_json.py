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
      f.write("%s\n" % json.dumps(x))