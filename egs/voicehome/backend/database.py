from pymongo import MongoClient

# Config the MongoDB data location at /etc/mongodb.conf (default: dbpath=/var/lib/mongodb)


class VoicehomeDatabase:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.mongo_client = MongoClient(self.cfg.mongo.host, self.cfg.mongo.port)
        self.db = self.mongo_client.voicehome
        print('Database: Initialized.')

    def write(self, module_name, payload):
        self.db[module_name].insert_one(payload)
        print('Saved to mongo.')

    def read(self, module_name, query):
        return [it for it in self.db[module_name].find(query)]
