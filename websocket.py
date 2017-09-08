from vityBot import bot

from tornado import web
from tornado import websocket
from tornado import ioloop
from tornado import httpserver

import json

format_error_msg = 'Invalid request format'


class Chat(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        bot = None # to be initialised on authorisation

    def on_message(self, message):
        try:
            request = json.loads(message)
        except Exception as e:
            # if json fails to parse string
            self.write_message(format_error_msg)

        if request.get('type') == 'auth':
            username = request['username']
            password = request['password']
            # do auth
        elif request.get('type') == 'query':
            # get response
        else:
            self.write_message(format_error_msg)
