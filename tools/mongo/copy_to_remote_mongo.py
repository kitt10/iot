from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient, errors as pymongo_errors

MONGO_HOST = "147.228.124.68"   # RPi
MONGO_DB = "smarthome"
MONGO_USER = "pi"
MONGO_PASS = "zkuspyvo"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)

client_local = MongoClient('localhost', 27017)
db_local = client_local.smarthome   # database
db_local_collection = db_local.testing   # collection

#topics = ('room/temperature', 'room/humidity', 'room/illuminance/', 'room/pressure', 'room/motion', 'room/door_open', 'room/window_open', 'outside/temperature')
topics = ('room/illuminance/',)
for topic_ending in topics:
    topic = 'smarthome/'+topic_ending
    print('Processing topic', topic)

    items = [item for item in db_local_collection.find({'topic': topic})]
    print(len(items), 'items found on local.')

    server.start()

    client_remote = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
    db_remote = client_remote[MONGO_DB]
    db_remote_collection = db_remote.testing

    for i, item in enumerate(items):
        if i % 1000 == 0:
            print((i+1), 'items processed.')
        try:
            db_remote_collection.insert_one(item)
        except pymongo_errors.DuplicateKeyError:
            pass

    print(len(items), 'items saved to mongo.')

    server.stop()