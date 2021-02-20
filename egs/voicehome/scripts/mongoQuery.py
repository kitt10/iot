import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

# myquery = { "key": "voicehome/sensors/temperature" }
myquery = { "_id": ObjectId('600b66a74b673e62da5d999f') }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)