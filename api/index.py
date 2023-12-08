import os
from http.server import BaseHTTPRequestHandler
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("DearXuan's API by python!".encode())
        newstr = self.GetNewStrFromNstr("instr")
        self.wfile.write(newstr.encode())
        return

    def GetNewStrFromNstr(self, instr):
        return "12345"
