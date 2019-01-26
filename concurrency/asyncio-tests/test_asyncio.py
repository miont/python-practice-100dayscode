"""
Example of asyncio usage for HTTP GET request processing and shell commands execution
Based on https://gist.github.com/ceralena/1e82a3ac140f402c9bd72a03ecba25c1#file-test_asyncio-py
"""

import asyncio
import aiohttp
from typing import Iterable

async def fetch_url(url:str):
    print(f'Start request to {url}...')
    async with aiohttp.ClientSession() as sess:
        async with sess.request('GET', url) as response:
            print(f'Finish request to {url}')
            print(f'Response status:{response.status}, {response.content_length} bytes received')
            return await response.text()

async def run_cmd(cmd:str):
    print(f'Start: {cmd}')
    proc = await asyncio.create_subprocess_shell(cmd, stdin=None, stdout=asyncio.subprocess.PIPE, stderr=None)
    print(f'Process created: {cmd}')
    out = await proc.stdout.read()
    print(f'Finish: {cmd}. Output: {out}')
    return out

async def run_all(urls:Iterable[str]=None, shellcmds:Iterable[str]=None):
    tasks = [fetch_url(url) for url in urls] + [run_cmd(cmd) for cmd in shellcmds]
    results = await asyncio.gather(*tasks)
    return results

def main():
    results = asyncio.run(run_all(urls=('http://google.com', 'http://google.com', 'http://yandex.ru', 'https://realpython.com'), shellcmds=('ls ~/', 'pwd', 'lsof -i:3000')))

    # for res in results:
    #     print(res)


if __name__=='__main__':
    main()
