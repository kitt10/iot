import tornado.ioloop
import tornado.web
import os
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class JsonHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(storage))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/json/", JsonHandler),
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    storage = {'data': [1, 2]}
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()