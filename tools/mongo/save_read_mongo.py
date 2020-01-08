from pymongo import MongoClient
from json import loads as json_loads

# Config the MongoDB data location at /etc/mongodb.conf (default: dbpath=/var/lib/mongodb)
def save2mongo(collection, item):
    collection.insert_one(item)
    print('Saved to mongo.')

def read_mongo(collection, topic):
    items = [item for item in collection.find({'topic': topic})]
    for item in items:
        print(json_loads(item['payload'].decode('utf-8')))

if __name__ == '__main__':
    mongoClient = MongoClient('localhost', 27077)
    db = mongoClient.smarthome   # database
    db_collection = db.testing   # collection

    msg_to_be_saved = {
        'topic': 'smarthome/room/temperature',
        'payload': {
            'sensor': 'ds18b20_01',
            'value': 38
        }
    }
    save2mongo(db_collection, item=msg_to_be_saved)

    read_mongo(db_collection, topic='smarthome/room/temperature')