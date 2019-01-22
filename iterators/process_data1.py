# Example from https://realpython.com/python-itertools/#sequences-of-numbers

from collections import namedtuple
import csv
from datetime import datetime
import itertools as it
import functools as ft
import operator as op
import argparse

class DataPoint(namedtuple('DataPoint', ['date', 'value'])):
    __slots__ = ()

    def __le__(self, other):
        return self.value <= other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value

def consecutive_positives(sequence, zero=0):
    def _consecutives():
        for itr in it.repeat(iter(sequence)):
            yield tuple(it.takewhile(lambda p: p > zero,
                                    it.dropwhile(lambda p: p <= zero, itr)))
    return it.takewhile(lambda t: len(t), _consecutives())

def read_prices(csvfile, _strptime=datetime.strptime):
    with open(csvfile) as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            yield DataPoint(date=_strptime(row['Date'], '%Y-%m-%d').date(),
                            value=float(row['Adj Close']))

def calc_percent_change(new_value, old_value):
    return 100*(new_value/old_value - 1.)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', help='Path to the input file', default='data/SP500.csv')
    args = parser.parse_args()
    return args

# Parse command line arguments
args = parse_args()
print('args:', args)

# Read prices and calculate daily percent change
prices = tuple(read_prices(args.input_file))
gains = tuple(DataPoint(date=day.date, value=calc_percent_change(day.value, prev_day.value)) 
              for day, prev_day in zip(prices[1:], prices))

# Find maximum daily gain/loss
zdp = DataPoint(None, 0)
max_gain = ft.reduce(max, it.filterfalse(lambda p: p <= zdp, gains))
max_loss = ft.reduce(min, it.filterfalse(lambda p: p > zdp, gains), zdp)

# max_gain = max(gains, key=lambda x:x.value)   # can do it this way 
# max_loss = min(gains, key=lambda x:x.value)

# Find longest growth streak
growth_streaks = consecutive_positives(gains, zero=DataPoint(None, 0))
longest_streak = ft.reduce(lambda x, y: x if len(x) > len(y) else y,
                          growth_streaks)

# Some stats about prices
max_overall = ft.reduce(max, prices)
min_overall = ft.reduce(min, prices)
mean_price = sum(p.value for p in prices)/len(prices)

# Display results
print('Max gain: {1:.2f}% on {0}'.format(*max_gain))
print('Max loss: {1:.2f}% on {0}'.format(*max_loss))

print('Longest growth streak: {num_days} days ({first} to {last}), {change:.2f}% total change'.format(
    num_days=len(longest_streak),
    first=longest_streak[0].date,
    last=longest_streak[-1].date,
    change=calc_percent_change(longest_streak[0].value, longest_streak[1].value)
))

print('History price maximum: {1} on {0}'.format(*max_overall))
print('History price minimum: {1} on {0}'.format(*min_overall))
print('Mean price: {:.2f}'.format(mean_price))

