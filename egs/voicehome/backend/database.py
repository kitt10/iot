from pymongo import MongoClient

# Linux conf: /etc/mongodb.conf
# Linux data: dbpath=/var/lib/mongodb
#
# Mac MONGODB installation:
#   $ brew tap mongodb/brew
#   $ brew install mongodb-community@4.4
# Mac conf: /usr/local/etc/mongod.conf
# Mac log: /usr/local/var/log/mongodb
# Mac data: /usr/local/var/mongodb
# Mac run MongoDB: $ brew services start mongodb-community@4.4
# Mac stop MongoDB: $ brew services start mongodb-community@4.4


class VoicehomeDatabase:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.mongo_client = MongoClient(self.cfg.mongo.host, self.cfg.mongo.port)
        self.db = self.mongo_client.voicehome
        print('Database: Initialized.')

    def write(self, module_id, payload):
        self.db[module_id].insert(payload)
        print('Saved to mongo.')

    def read(self, module_id, query):
        return [it for it in self.db[module_id].find(query)]
