from tornado.web import RequestHandler
from tornado.escape import json_decode
from os.path import join
from json import dumps as json_dumps

class EP_Data(RequestHandler):
    
    def initialize(self, app):
        self.app = app

    def post(self):
        query = json_decode(self.request.body)
        self.write(self.app.db.get_data(limit=query['limit']))

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")