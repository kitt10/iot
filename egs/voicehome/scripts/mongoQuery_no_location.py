import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["voicehome"]
mycol = mydb["sensors"]

# define empty list
places = []
# open file and read the content in a list
with open('mongo_update_no_location.txt', 'r') as filehandle:
    places = [current_place.rstrip() for current_place in filehandle.readlines()]


for place in places:

    # find by topic
    # myquery = { "key": "voicehome/sensors/temperature" }
    # find by id
    myquery = { "_id": ObjectId(place) }


    mydoc = mycol.find(myquery)

    for x in mydoc:
        print(x)