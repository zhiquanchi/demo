from fastapi import FastAPI, Response,APIRouter, Depends,Form
from sse_starlette.sse import EventSourceResponse
import asyncio
import random
import json
from pydantic import BaseModel


admin_router = APIRouter(prefix='/admin')

# 这个函数用来获取运行环境中的本机地址和端口
def get_host():
    import socket
    host = socket.gethostbyname(socket.gethostname())
    return f"http://{host}:8000"


@admin_router.get('/')
async def main(get_host=Depends(get_host)):
    # 生成一个登录页面，账号密码分别为admin和admin，账号密码在前端校验。登录成功后跳转到home页面

    html = f"""
    <html>
    <head>
        <title>admin</title>
    </head>
    <body>
        <form action="/admin/home" method="post">
            <label for="username">username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    return Response(content=html, media_type="text/html")

@admin_router.post('/home')
async def home(username:str=Form(...),password:str=Form(...) ):
    # 如果账号密码正确，返回home页面，否则返回登录页面
    if username == 'admin' and password == 'admin':
        html = """
        <html>
        <head>
            <title>后台管理系统</title>
            <script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
        </head>
        <body>
            <h1>后台管理系统</h1>
            
            <div id="qrcode"></div>
            
        <button onclick="createRoom()">创建会场</button>
        <button onclick="down()">下载竞拍数据</button>
        <button onclick="qrcode()">生成二维码</button>
        
        </body>
        <script>
            
        
            function createRoom() {{
                fetch('/admin/create_room')
                .then(response => response.json())
                .then(data => {{
                    alert('创建成功，会场号为：' + data.room_id)
                }})
            }}
            
            function down() {{
            alert('下载成功,测试版本暂不支持下载功能')
            }}
            
            function qrcode() {{
            var qrcode = new QRCode(document.getElementById("qrcode"), {
            text: "后期会替换为竞拍链接",
            width: 128,
            height: 128,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
                });
        }}
        </script>
        </html>
        """
        return Response(content=html, media_type="text/html")
    else:
        return Response(content="username or password error", media_type="text/html")

@admin_router.get('/create_room')
async def create_room():
    # 创建一个会场
    room_id = random.randint(10001, 10030)
    print(f"create room {room_id}")
    return {"room_id": room_id}
