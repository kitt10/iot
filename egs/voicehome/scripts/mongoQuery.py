import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

# myquery = { "key": "voicehome/sensors/temperature" }
myquery = { "_id": '600b671f4b673e62da5d99a3' }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)