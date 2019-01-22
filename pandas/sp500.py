# SP500 historic data analysis with Pandas
import argparse
import numpy as np
import pandas as pd
from collections import namedtuple

DataPoint = namedtuple('DataPoint', ['date', 'value'])

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', help='Path to the input file', default='data/SP500.csv')
    args = parser.parse_args()
    return args

# Parse command line arguments
args = parse_args()

# Read data
df = pd.read_csv(args.input_file, index_col=0)

# Calculate daily gains
df['gain'] = 100*(df['Adj Close']/df['Adj Close'].shift(1) - 1.)
df['gain'].iloc[0] = 0
print(df.head(10))

# Find maximum gain and lose
max_gain = DataPoint(date=df['gain'].idxmax(), value=df['gain'].max())
max_loss = DataPoint(date=df['gain'].idxmin(), value=df['gain'].min())
# print(df.describe())

# Find longest growthing streak


# Display results
print('Max gain: {1:.2f}% on {0}'.format(*max_gain))
print('Max loss: {1:.2f}% on {0}'.format(*max_loss))