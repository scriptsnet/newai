# vercel_api.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
import httpx
import os  # 引入 os 模块

app = FastAPI()

# 获取环境变量中的 OpenAI API 端点和密钥
openai_api_endpoint = os.environ.get("OPENAI_API_ENDPOINT")
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_endpoint or not openai_api_key:
    raise ValueError("OPENAI_API_ENDPOINT or OPENAI_API_KEY environment variables are not set")

# 获取环境变量中的国内 API 接口地址
domestic_api_url = os.environ.get("DOMESTIC_API_URL")
if not domestic_api_url:
    raise ValueError("DOMESTIC_API_URL environment variable is not set")

# 接收国内 API 请求并转发到 OpenAI
@app.post("/openai/request")
async def forward_to_openai(request: Request):
    try:
        # 获取国内 API 请求的数据
        data = await request.json()

        # 转发请求到 OpenAI
        async with httpx.AsyncClient() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"  # 设置OpenAI API密钥
            }
            response = await client.post(openai_api_endpoint, json=data, headers=headers)

        # 获取 OpenAI 的响应数据
        openai_response_data = response.json()

        # 将 OpenAI 的响应数据转发到国内 API 接口
        async with httpx.AsyncClient() as client:
            await client.post(domestic_api_url, json=openai_response_data)

        return JSONResponse(content={"message": "Request processed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# 新增一个路由，返回简单的信息
@app.get("/welcome")
async def welcome():
    return HTMLResponse(content="<h1>Welcome to the API!</h1>")
