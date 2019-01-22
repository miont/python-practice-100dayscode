## Requesting data on future events from www.eventbriteapi.com
## Single thread version
import requests
from datetime import datetime, timedelta
import time
import json
from collections import defaultdict
from typing import Iterable

TOKEN = 'NCOER2SNWAZCXEWQU2EZ'

DATETIME_FORMAT = '%Y-%m-%dT%H:%m:%S'

def process_response(res:requests.Response):
    struct = res.json()
    events = []
    try:
        for event in struct['events']:
            event_info = {'name': event['name']['text'], 'description': event['description']['text'], 'url': event['url']}
            events.append(event_info)
    except Exception as e:
        print(e)
    return events

def compose_events_search_req(start_datetime:datetime, end_datetime:datetime):
    start_datetime_str = start_datetime.strftime(DATETIME_FORMAT)
    end_datetime_str = end_datetime.strftime(DATETIME_FORMAT)
    return '''https://www.eventbriteapi.com/v3/events/search/?token={token}&start_date.range_start={start}&start_date.range_end={end}'''.format(token=TOKEN, start=start_datetime_str, end=end_datetime_str)

def make_request(session, start:datetime, end:datetime):
    url = compose_events_search_req(start, end)
    print('making request to', url)
    res = session.request(method='GET', url=url)
    data = process_response(res)
    return data

def make_all_requests(days:int=10):
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
    with requests.Session() as sess:
        for _ in range(days):
            # Time bounds for event search
            start = end
            end = start + timedelta(days=1) - timedelta(minutes=1)
            res = make_request(session=sess, start=start, end=end)
            events[start.date()] = res
    return events

def print_events(events:Iterable):
    for date in events.keys():
        for event in events[date]:
            print('{}: {}'.format(date, event['name']))

def count_events(events:Iterable):
    return sum(len(events[date]) for date in events.keys())

if __name__ == '__main__':
    start_time = time.time()
    events = make_all_requests(days=10)
    elapsed_time = time.time() - start_time
    print('All events:', events)
    print_events(events)
    print('Elapsed time: {:.2f}s. Total events count: {}'.format(elapsed_time, count_events(events)))