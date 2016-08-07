import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r'/', MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": PEMFILE,
        "keyfile": KEYFILE
    })
    http_server.listen(443)
    tornado.ioloop.IOLoop.current().start()
