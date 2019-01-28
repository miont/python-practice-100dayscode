import asyncio
import itertools
import time
import sys

class Signal:
    go = True

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))      

async def slow_function(n):
    await asyncio.sleep(n)
    return 77

async def supervisor():
    spinner = asyncio.create_task(spin('waiting...'))
    print('spinner object:', spinner)
    result = await slow_function(4)
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(supervisor())
    finally:
        loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()