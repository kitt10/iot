import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

# myquery = { "address": { "$regex": "^S" } }
myquery = { "_id": ObjectId('600b66a74b673e62da5d999f') }
newvalues = { "$set": { "payload": '{"location": "room_1", "owner": "jsanda", "status": "ok", "sensor_id": "room_1", "quantity": "degrees", "timestamp": "2021-01-23 00:58:31", "temperature_value": 18.83333}' } }

x = mycol.update(myquery, newvalues)

print(x.modified_count, "documents updated.")