import os
import json
from http.server import BaseHTTPRequestHandler
import openai
from flask import Flask, redirect, render_template, request, url_for
from urllib.parse import parse_qs

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class handler(BaseHTTPRequestHandler):
    conversation_history = [
        {"role": "system", "content": "你是一个非常厉害的工作助手，你无所不能"},
    ]

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode())

        word = params.get('word', [''])[0]
        history = params.get('history', [''])[0]
        redirect_uri = params.get('redirect_uri', [''])[0]
        ownid = params.get('ownid', [''])[0]

        #self.conversation_history.append({"role": "user", "content": history})

        response = self.send_message(word)
        resp = {
            "response": response,
            "ownid": ownid
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())

    def send_message(self, message):
        try:
            self.conversation_history.append({"role": "user", "content": message})

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.conversation_history
            )

            assistant_reply = response['choices'][0]['message']['content']
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})

            return assistant_reply
        except Exception as e:
            return f"Error occurred while processing the request: {e}"
