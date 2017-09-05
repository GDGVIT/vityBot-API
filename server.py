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
        print "Connection open"

    def on_message(self, message):
        # self.message = message
        self.write_message("your question is " + message)

    def on_close(self):
        print "connection closed"
        if self in cl:
            cl.remove(self)
            # self.write_message("connection closed by server")


class ApiHandler(RequestHandler):
    """api side"""

    @coroutine
    def get(self):
        pass


settings = dict(
    # debug=True
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
