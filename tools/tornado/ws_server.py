from tornado.web import StaticFileHandler, RequestHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from os.path import dirname, join as join_path
from json import dumps as dumps_json, loads as loads_json


class MainHandler(RequestHandler):
    def get(self):
        self.render("static/index_css_js_ws.html")


class WSHandler(WebSocketHandler):

    def initialize(self):
        self.application.ws_clients.append(self)
        print('Webserver: New WS Client. Connected clients:', len(self.application.ws_clients))

    def open(self):
        print('Webserver: Websocket opened.')
        self.write_message('Server ready.')

    def on_message(self, msg):
        try:
            msg = loads_json(msg)
            print('Webserver: Received json WS message:', msg)
        except (ValueError):
            print('Webserver: Received WS message:', msg)

    def on_close(self):
        self.application.ws_clients.remove(self)
        print('Webserver: Websocket client closed. Connected clients:', len(self.application.ws_clients))

class WebWSApp(TornadoApplication):

    def __init__(self):
        self.ws_clients = []

        self.tornado_handlers = [
            (r'/', MainHandler),
            (r'/websocket', WSHandler),
            (r'/(.*)', StaticFileHandler, {'path': join_path(dirname(__file__), 'static')})
        ]
        self.tornado_settings = {
            "debug": True,
            "autoreload": True
        }
        TornadoApplication.__init__(self, self.tornado_handlers, **self.tornado_settings)

    def send_ws_message(self, message):
        for client in self.ws_clients:
            iol.spawn_callback(client.write_message, dumps_json(message))


if __name__ == '__main__':
    PORT = 8881

    app = WebWSApp()
    app.listen(PORT)
    iol = IOLoop.current()
    iol.start()
    print('Webserver: Initialized. Listening on', PORT)
