#! /usr/bin/env python3

# Author: Thomas Gruber
# Version: 0.93, 11/06/18

from http.server import HTTPServer, BaseHTTPRequestHandler
from movement import MovementManager

import io
import json
import time


HTTP_PORT = 80


class Singleton (type):
    _instances = {}

    def __call__(cls, *args, **kargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kargs)
        return cls._instances[cls]


class ServerCache (metaclass=Singleton):

    INITIAL_CMD = 0

    def __init__(self):
        self.movement_manager = MovementManager()
        self.is_collecting = False
        self.previous_command = self.INITIAL_CMD


class ControlHandler (BaseHTTPRequestHandler):
    SERVER_PATH = '/terradrone'
    CHAR_ENCODING = 'utf-8'

    # HTTP response codes
    ACCEPTED_RESPONSE                   = 202
    BAD_REQUEST_RESPONSE                = 400
    UNAUTHROIZED_RESPONSE               = 401
    TEAPOT_RESPONSE                     = 418

    # commands should correspond to those written in Android application
    CMD_ERROR                           = 0
    CMD_TEST                            = 1
    CMD_FORWARD_START                   = 100
    CMD_FORWARD_STOP                    = 101
    CMD_BACKWARD_START                  = 102
    CMD_BACKWARD_STOP                   = 103
    CMD_ROTATE_RIGHT_START              = 104
    CMD_ROTATE_RIGHT_STOP               = 105
    CMD_ROTATE_LEFT_START               = 106
    CMD_ROTATE_LEFT_STOP                = 107
    CMD_COLLECT                         = 200


    cache = ServerCache()


    def do_GET(self):
        # deny request
        self.send_error(self.TEAPOT_RESPONSE)


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        json_bytes = self.rfile.read(content_length).decode(self.CHAR_ENCODING)

        request = json.loads(json_bytes)
        request_type = request['command']

        # only allow requests with correct path (weak security feature)
        if self.path == self.SERVER_PATH:
            if request_type == self.CMD_TEST:
                response = {
                    'time': self.get_time(),
                    'command': self.CMD_TEST
                }

                self.send_accepted_response(response)

            elif request_type == self.CMD_COLLECT:
                # send fake response until auger motor is set up
                response = {
                    'time': self.get_time(),
                    'command': self.CMD_COLLECT,
                    'location': {
                        'latitude': 39.7596265,
                        'longitude': -84.1230534
                    }
                }

                self.send_accepted_response(response)

            elif request_type == self.CMD_FORWARD_START:
                if not self.cache.movement_manager.is_moving or not self.cache.is_collecting:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.forward()

            elif request_type == self.CMD_FORWARD_STOP:
                if self.cache.previous_command == self.CMD_FORWARD_START:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.stop()

            elif request_type == self.CMD_BACKWARD_START:
                if not self.cache.movement_manager.is_moving or not self.cache.is_collecting:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.backward()

            elif request_type == self.CMD_BACKWARD_STOP:
                if self.cache.previous_command == self.CMD_BACKWARD_START:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.stop()

            elif request_type == self.CMD_ROTATE_RIGHT_START:
                if not self.cache.movement_manager.is_moving or not self.cache.is_collecting:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.rotate_right()

            elif request_type == self.CMD_ROTATE_RIGHT_STOP:
                if self.cache.previous_command == self.CMD_ROTATE_RIGHT_START:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.stop()

            elif request_type == self.CMD_ROTATE_LEFT_START:
                if not self.cache.movement_manager.is_moving or not self.cache.is_collecting:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.rotate_left()

            elif request_type == self.CMD_ROTATE_LEFT_STOP:
                if self.cache.previous_command == self.CMD_ROTATE_LEFT_START:
                    self.cache.previous_command = request_type
                    self.cache.movement_manager.stop()

            else:
                # invalid command type
                self.send_error(self.BAD_REQUEST_RESPONSE)

        else:
            self.send_error(self.UNAUTHROIZED_RESPONSE)

        # default to closing all connections
        self.close_connection = True


    def send_accepted_response(self, response):
        json_response = json.dumps(response).encode(self.CHAR_ENCODING)

        content_buffer = io.BytesIO()
        response_length = content_buffer.write(json_response)

        self.send_response(self.ACCEPTED_RESPONSE)
        self.send_header('Content-Length', response_length)
        self.send_header('Content-Type', 'application/json; charset=' + self.CHAR_ENCODING)
        self.send_header('Connection', 'close')
        self.end_headers()

        self.wfile.write(content_buffer.getvalue())
        content_buffer.close()


    def get_time(self):
        return int(round(time.time() * 1e3))


def main():
    print('Starting HTTP server on port 80.')
    print('Awaiting requests...')

    # must be ran with 'sudo' to run on port 80
    httpd = HTTPServer(('', HTTP_PORT), ControlHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
