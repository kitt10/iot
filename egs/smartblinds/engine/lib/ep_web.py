from tornado.web import RequestHandler
from os.path import join

class EP_Web(RequestHandler):
    
    def initialize(self, webserver):
        self.ws = webserver

    def get(self):
        if self.ws.host_web:
            self.render(join(self.ws.static_path_rel, self.ws.static_index))
        else:
            self.write('The web is not hosted here.')
