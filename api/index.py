from http.server import BaseHTTPRequestHandler
import openai
import os

# 从环境变量获取你的OpenAI Secret Key，如果没有设置，使用默认值
openai.api_key = os.getenv("OPENAI_SK", "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")  

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
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
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())
        return
