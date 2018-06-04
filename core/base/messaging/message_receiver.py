#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from core.api.system.system import System
from core.api.survey.survey import Survey
from core.base.messaging.message_sender import MessageSender
from core.api.util.util import Util
import json


class MessageHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        response = None

        if self.path == '/collect-sysinfo':
            with open(System.Agent.sys_out_path()) as f:
                d = json.load(f)
                result = json.dumps(d) # to str
            # Send result to alfa server.
            print(result)
            ms = MessageSender(Util.server_url() + "sysinfo-result")
            ms.send(result)
        elif self.path == '/create-survey':
            content_length = int(self.headers['Content-Length'])
            content = self.rfile.read(content_length)
            body = json.loads(content.decode('utf-8'))
            survey_json = body['survey']
            survey_id = body['survey_id']
            survey = Survey(survey_json, survey_id)
            self._set_headers()
            self.wfile.write("{ \"response\": \"request received. processing...\"}".encode('utf-8'))
            # Result will be sent to alfa server when user completes the survey.
            survey.show()
            return

        self._set_headers()
        self.wfile.write("{ \"response\": \"request received. processing...\"}".encode('utf-8'))
