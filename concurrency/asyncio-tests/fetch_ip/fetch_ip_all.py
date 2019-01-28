"""
Request your IP.
Based on:
https://hackernoon.com/asyncio-for-the-working-python-developer-5c468e6e2e8e
https://stackoverflow.com/questions/50900832/is-calling-ensure-future-the-right-way-to-wrap-up-the-results-of-coroutines
"""

from collections import namedtuple
import time
import asyncio
from concurrent.futures import FIRST_COMPLETED
import aiohttp
from common import *

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('ipinfo', 'https://ipinfo.io/json', 'ip')
)

async def main():
    tasks = {service.name: fetch_ip(service) for service in SERVICES}
    results = await asyncio.gather(*tasks.values())
    results = {k: results[i] for i, k in enumerate(tasks.keys())}
    print('Results:', results)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()