from tornado.web import RequestHandler
from tornado.escape import json_decode
from os.path import join
from json import dumps as json_dumps

class EP_Control(RequestHandler):
    
    def initialize(self, app):
        self.app = app

    def post(self):
        query = json_decode(self.request.body)
        position, tilt = self.app.cl.get_control(classifier_name=query['classifier_name'], features=query['features'])
        self.write(json_dumps({'data': {'position': position, 'tilt': tilt}}))
