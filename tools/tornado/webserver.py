from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from os.path import join, dirname
import json


class MainHandler(RequestHandler):
    def get(self):
        self.render("static/index.html")


class JsonHandler(RequestHandler):
    def get(self):
        self.write(json.dumps(storage))


class WebApp(Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/json/", JsonHandler),
            ('/(.*)', StaticFileHandler, {'path': join(dirname(__file__), 'static')})
        ]
        settings = {
            "debug": True
        }
        Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    storage = {'data': [1, 2]}
    app = WebApp()
    app.listen(8888)
    IOLoop.current().start()
