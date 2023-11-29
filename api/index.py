from http.server import BaseHTTPRequestHandler
import openai
import os

openai.api_key = os.getenv("OPENAI_SK", "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")  

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = openai.ChatCompletion.create(
            model="gpt-4.0-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "你的版本是多少？"
                }
            ]
        )

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response['choices'][0]['message']['content'].encode())
        return
