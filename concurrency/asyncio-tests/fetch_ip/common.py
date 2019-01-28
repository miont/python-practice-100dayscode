from collections import namedtuple
import time
import asyncio
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

async def aiohttp_get_json(url):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as response:
            return await response.json()

async def fetch_ip(service):
    start = time.time()
    print(f'Fetching IP from {service.name}')
    json_response = await aiohttp_get_json(service.url)
    ip = json_response[service.ip_attr]
    elapsed = time.time() - start
    print(f'{service.name} finished with result: {ip}, took {elapsed:.2f} seconds')
    return ip