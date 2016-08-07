import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

from settings import *


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        logging.debug(json.dumps(self.request))

application = tornado.web.Application([
    (r'/', MainHandler),
])

if __name__ == "__main__":
    define("port", default="443", help="Port to listen on")
    define("host", default="localhost", help="Server address to listen on")
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": PEMFILE,
        "keyfile": KEYFILE
    })
    http_server.listen(int(options.port), address=options.host)
    tornado.ioloop.IOLoop.current().start()
