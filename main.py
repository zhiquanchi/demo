from fastapi import FastAPI, Response
from sse_starlette.sse import EventSourceResponse
import asyncio
import random
import json
from pydantic import BaseModel

from demotest.submit import main
from admin.admin import admin_router


class Item(BaseModel):
    id: str = '10001'
    value: int = 10


app = FastAPI()
app.include_router(admin_router)


# 这个路由返回demo.html页面
@app.get("/")
async def read_root():
    with open("demo.html", "r", encoding='utf-8') as f:
        html = f.read()
    return Response(content=html, media_type="text/html")


# 用来保存提交的数据，设置为全局变量
items = {}


@app.post("/submit")
async def submit(item: Item):
    # 将提交进来的Item保存到items字典中,如果items字典中已经存在这个item.id,则将这个item.id的value和新提交的item.value相加

    if item.id in items.keys():
        items[item.id] += item.value
    else:
        items[item.id] = item.value
    # 返回更新后的数据
    return items
    # return {item.id: item.value}


@app.post("/start")
async def start():
    await main()


@app.post("/reset")
async def reset():
    items.clear()

    async def generator():
        yield json.dumps(items)

    return EventSourceResponse(generator())


@app.get("/stream")
async def message_stream(response: Response):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    # async def event_generator():
    #     items = [f"Item {i}" for i in range(1, 601)]
    #     while True:
    #         await asyncio.sleep(1)  # 每秒发送一次数据
    #         random_item = random.choice(items)
    #         random_value = random.randint(1, 1000)
    #         data = {"name": random_item, "value": random_value}
    #         yield json.dumps(data)

    # 每当 items 发生变化时，就会发送一次数据
    async def event_generator():
        while True:
            await asyncio.sleep(0.5)
            for key, value in items.items():
                data = {"name": key, "value": value}
                yield json.dumps(data)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
