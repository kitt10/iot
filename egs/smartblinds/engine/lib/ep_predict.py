from tornado.web import RequestHandler
from tornado.escape import json_decode
from os.path import join
from json import dumps as json_dumps
from numpyencoder import NumpyEncoder

class EP_Predict(RequestHandler):
    
    def initialize(self, app):
        self.app = app

    def post(self):
        query = json_decode(self.request.body)
        ts_start = query.get('ts_start', None)
        ts_end = query.get('ts_end', None)
        classifiers = query.get('classifiers', ['ifelse', 'ffnn', 'lstm'])
        
        if ts_start and ts_end:
            data = list(self.app.db.collection.find({'timestamp': {'$gte': ts_start, '$lte': ts_end}}).sort('timestamp', 1))
        elif ts_start:
            data = list(self.app.db.collection.find({'timestamp': {'$gte': ts_start}}).sort('timestamp', 1))
        elif ts_end:
            data = list(self.app.db.collection.find({'timestamp': {'$lte': ts_end}}).sort('timestamp', 1))
        else:
            data = list(self.app.db.collection.find().sort('timestamp', 1))
        payload = dict()
        for cl in classifiers:
            payload[cl] = self.app.cl.predict(classifier_name=cl, data = data)
        payload['status'] = 'ok'
        self.write(json_dumps({'payload': payload}, cls=NumpyEncoder))
        
    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")