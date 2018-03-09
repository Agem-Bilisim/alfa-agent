#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from core.api.system.system import System
import json


class MessageHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        response = None

        if self.path == '/collect-sysinfo':
            with open(System.Agent.sys_out_path()) as f:
                d = json.load(f)
                s = json.dumps(d) # to str
            response = s.encode('utf-8') #base64.b64encode(s.encode('utf-8'))
        elif self.path == 'create-survey':
            content_length = int(self.headers['Content-Length'])
            content = self.rfile.read(content_length)
            body = json.load(content)
            survey_json = body['survey_json']
            # TODO call survey.py

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(response)
