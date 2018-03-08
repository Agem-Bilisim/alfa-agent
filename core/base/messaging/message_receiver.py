#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from io import BytesIO
from core.api.system.system import System
import json
import base64


class MessageHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.load(self.rfile.read(content_length))

        response = BytesIO()
        if self.path == 'collect-sysinfo':
            with open(System.Agent.sys_out_path()) as f:
                d = json.load(f)
                s = json.dumps(d) # to str
            response.write(base64.b64encode(s.encode('utf-8')))
        elif self.path == 'create-survey':
            pass
            # TODO get survey params

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(response.getvalue())
