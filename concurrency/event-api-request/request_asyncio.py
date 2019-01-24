import time
from datetime import timedelta
import asyncio
import aiohttp
import json
from collections import defaultdict
from typing import Iterable
from common import *


async def make_request(session, start:datetime, end:datetime):
    url = compose_events_search_req(start, end)
    print('making request to', url)
    async with session.get(url) as response:
        if response.status == 200:
            data = process_response(await response.json())
        else:
            pass # TODO: use logger here
    return data

def process_response(res:dict):
    """
    Do some operations with response
    Args:
        res: response in json format
    """
    struct = res
    events = []
    try:
        for event in struct['events']:
            event_info = {'name': event['name']['text'], 'description': event['description']['text'], 'url': event['url']}
            events.append(event_info)
    except Exception as e:
        print(e)
    return events

async def make_all_requests(days:int=10):
    """
    Making all the requests
    Args:
        days: how many days starting from today we want to get events
    """
    now = datetime.now()
    start = datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    end = start
    events = defaultdict(list)
    print('Retrieving all events starting from', start.date)
    async with aiohttp.ClientSession() as session:
        tasks = []
        dates = []
        for i in range(days):
            # Time bounds for event search
            start = end
            end = start + timedelta(days=1) - timedelta(minutes=1)
            task = asyncio.ensure_future(make_request(session, start, end))
            tasks.append(task)
            dates.append(start.date())
        await asyncio.gather(*tasks, return_exceptions=True)

    for task, date in zip(tasks, dates):
        events[date] = task.result()
            
    return events

if __name__ == '__main__':
    start_time = time.time()
    events = asyncio.get_event_loop().run_until_complete(make_all_requests(days=10))
    elapsed_time = time.time() - start_time
    print('All events:', events)
    print_events(events)
    print('Elapsed time: {:.2f}s. Total events count: {}'.format(elapsed_time, count_events(events)))