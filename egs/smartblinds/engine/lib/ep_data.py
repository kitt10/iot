from tornado.web import RequestHandler
from tornado.escape import json_decode
from os.path import join
from json import dumps as json_dumps

class EP_Data(RequestHandler):
    
    def initialize(self, app):
        self.app = app

    def post(self):
        query = json_decode(self.request.body)
        data = self.app.db.get_data(limit=query['limit'])
        self.write(json_dumps({'data': data}))
