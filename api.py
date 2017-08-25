from tornado.web import RequestHandler, Application, removeslash
from tornado.gen import coroutine
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

# other libraries
import json
import os
import env
from motor import MotorClient as Client
import uuid
import base64
import requests

cl = []
db = Client(env.DB_LINK)['vitybot-user-session']


class User(object):
    username = ""
    password = ""
    is_logged_in = False
    session_id = None

    @staticmethod
    def student_info(regNo, passwd):
        url = "https://myffcs.in:10443/campus/vellore/personalDetails"
        params = dict(regNo=regNo, passwd=passwd)
        res = requests.post(url, params=params)
        return res.status_code == 200


class IndexHandler(RequestHandler, User):
    @coroutine
    @removeslash
    def get(self):

        if self.get_secure_cookie('username') is None:
            print "not found cookies"
            User.is_logged_in = False
            self.redirect('/log')

        else:
            print "found cookies"
            User.username = self.get_secure_cookie('username')
            User.password = self.get_secure_cookie('password')
            User.session_id = self.get_secure_cookie('session_id')
            User.is_logged_in = True
            self.redirect('/node')


class Log(RequestHandler):
    @coroutine
    @removeslash
    def get(self):

        """
        success = 'failed' in case of login unsuccessful
        else redirecting to node
        :return:
        """

        try:
            msg = self.get_query_argument('success')

        except:
            msg = ""
        self.render('login.html', success=msg)


class LoginHandler(RequestHandler, User):
    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        if not User.student_info(username, password):
            self.redirect('/log?success=False')

        User.username = username
        User.password = password

        print User.username

        self.set_secure_cookie('username', User.username)
        self.set_secure_cookie('password', User.password)

        self.redirect('/node')


class BaseHandler(RequestHandler, User):
    def get(self):
        self.write(User.username + User.password)


class SocketHandler(WebSocketHandler):
    def open(self):
        if self not in cl:
            cl.append(self)
        print "Connection open"

    def on_message(self, message):
        # self.message = message
        self.write_message(message)

    def on_close(self):
        print "connection closed"
        if self in cl:
            cl.remove(self)
            # self.write_message("connection closed by server")


settings = dict(
    # debug=True,
    cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
)

app = Application(
    handlers=[
        (r'/', IndexHandler),
        (r'/log', Log),
        (r'/node', BaseHandler),
        (r'/login', LoginHandler),
        (r'/ws', SocketHandler),
        (r'/api', BaseHandler)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    **settings)

if __name__ == "__main__":
    server = HTTPServer(app)
    server.listen(8080)
    IOLoop.instance().start()
