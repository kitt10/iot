from ._tools import format_secs
from ._database import generate_random_data
from datetime import datetime
from time import time
from pymongo import MongoClient
from bson.json_util import dumps as json_dumpsb
import numpy as np

class Database:

    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        self.host = self.cfg['database']['host']
        self.port = self.cfg['database']['port']
        self.db_name = self.cfg['database']['name']
        self.coll_name = self.cfg['database']['collection']
        self.real_data = self.cfg['database']['real_data']
        self.verbose = self.cfg['database']['verbose']
        self.db_load_data_time = 0

        # Init MongoDB Connection
        self.client = MongoClient(self.host, self.port)
        self.collection = self.client[self.db_name][self.coll_name]

    def get_data(self, ts_start=0, ts_end=0):
        print('getting data in DB:', ts_start, ts_end)
        t0 = time()
        if self.real_data:
            if ts_start and ts_end:
                data = json_dumpsb({'data': list(self.collection.find({'timestamp': {'$gte': ts_start, '$lte': ts_end}}).sort('timestamp', 1))})
                self.log('Using data from '+str(datetime.fromtimestamp(ts_start))+' to '+str(datetime.fromtimestamp(ts_end)))
            elif ts_start:
                data = json_dumpsb({'data': list(self.collection.find({'timestamp': {'$gte': ts_start}}).sort('timestamp', 1))})
                self.log('Using data from '+str(datetime.fromtimestamp(ts_start)))
            elif ts_end:
                data = json_dumpsb({'data': list(self.collection.find({'timestamp': {'$lte': ts_end}}).sort('timestamp', 1))})
                self.log('Using data to '+str(datetime.fromtimestamp(ts_end)))
            else:
                data = json_dumpsb({'data': list(self.collection.find().sort('timestamp', 1))})
                self.log('Using all data')
        else:
            data = sorted(generate_random_data(days=1), key=lambda x:x['timestamp'], reverse=True)
            self.log('Using simulation random data.')
        self.db_load_data_time = time()-t0
        self.log('Data collected in '+format_secs(self.db_load_data_time))
        return data

    def log(self, buf):
        if self.verbose:
            print(datetime.now(), 'DB LOG:', buf)
