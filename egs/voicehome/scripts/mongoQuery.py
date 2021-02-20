import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

myquery = { "key": "voicehome/sensors/temperature" }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)