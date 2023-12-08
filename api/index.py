import os
from http.server import BaseHTTPRequestHandler
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

class handler(BaseHTTPRequestHandler):
    conversation_history = [
        {"role": "system", "content": "你是一个非常厉害的工作助手，你无所不能"},
    ]

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        #self.wfile.write("DearXuan's API by python!".encode())
        prompt = "请作诗一首"
        response = self.send_message(prompt)
        self.wfile.write(response.encode())
        return

    def send_message(self, message):
        self.conversation_history.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=self.conversation_history
        )

        assistant_reply = response['choices'][0]['message']['content']
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
