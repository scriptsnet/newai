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
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("DearXuan's API by python!".encode())
            prompt = "你是什么版本的GPT?"
            response = self.send_message(prompt)
            self.wfile.write(response.encode())
        except Exception as e:
            error_message = f"Error occurred: {e}"
            self.wfile.write(error_message.encode())
        return

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
