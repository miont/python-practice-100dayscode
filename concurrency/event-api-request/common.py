import requests
from datetime import datetime
from typing import Iterable

TOKEN = 'NCOER2SNWAZCXEWQU2EZ'

DATETIME_FORMAT = '%Y-%m-%dT%H:%m:%S'

def compose_events_search_req(start_datetime:datetime, end_datetime:datetime):
    start_datetime_str = start_datetime.strftime(DATETIME_FORMAT)
    end_datetime_str = end_datetime.strftime(DATETIME_FORMAT)
    return '''https://www.eventbriteapi.com/v3/events/search/?token={token}&start_date.range_start={start}&start_date.range_end={end}'''.format(token=TOKEN, start=start_datetime_str, end=end_datetime_str)

def print_events(events:Iterable):
    for date in events.keys():
        for event in events[date]:
            print('{}: {}'.format(date, event['name']))

def count_events(events:Iterable):
    return sum(len(events[date]) for date in events.keys())