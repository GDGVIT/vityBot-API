from tornado.web import RequestHandler, Application
from tornado.gen import coroutine
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import json
import os

cl = []

class IndexHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render('index.html')

class SocketHandler(WebSocketHandler):
    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        self.write_message('Your question is ' + message)

    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(RequestHandler):
    """api side"""
    @coroutine
    def get(self):
        pass

settings = dict(
    debug=True
)


app = Application(
    handlers=[
        (r'/', IndexHandler),
        (r'/ws', SocketHandler),
        (r'/api', ApiHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        **settings)
if __name__ == "__main__":
    server = HTTPServer(app)
    server.listen(8080)
    IOLoop.instance().start()
