from tornado.web import RequestHandler
from tornado.escape import json_decode
from os.path import join
from json import dumps as json_dumps

class EP_Train(RequestHandler):
    
    def initialize(self, app):
        self.app = app

    def post(self):
        try:
            payload = self.app.cl.train_now()
            payload.update({'status': 'ok'})
            self.write(json_dumps({'payload': payload}))
        except:
            print('Exception in the training part.')
            self.write(json_dumps({'payload': {'status': 'error training'}}))
            

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")