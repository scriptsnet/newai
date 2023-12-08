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
        prompt = "请将这句话翻译中英语“山有多高，地有多险，人心就有多高”"
        response = self.get_gpt3_response(prompt)
        self.wfile.write(response.encode())
        return

    def get_gpt3_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def GetNewStrFromNstr(self, instr):
        return "12345"
