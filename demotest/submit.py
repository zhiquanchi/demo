import aiohttp
import asyncio
import random
import json

async def send_request(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    url = "http://localhost:8000/submit"
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(5000):
            item_id = str(random.randint(10001, 10030))
            item_value = random.randint(1, 10)
            data = {"id": item_id, "value": item_value}
            tasks.append(send_request(session, url, data))
        responses = await asyncio.gather(*tasks)
        # for response in responses:
        #     print(response)

if __name__ == '__main__':

    # Python 3.7+
    asyncio.run(main())
    print("done")