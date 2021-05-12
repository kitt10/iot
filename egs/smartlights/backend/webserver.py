import tornado.ioloop
import tornado.web
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../frontend/index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {
                'path': os.path.join(os.path.dirname(__file__), '../frontend')})
        ]
        settings = {
            "debug": True,
            "autoreload": True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(4000)
    tornado.ioloop.IOLoop.current().start()