# Some analytics with the data from Elo Merchant Category Recommendation Kaggle competition
import numpy as np
import pandas as pd

train = pd.read_csv('data/elo_merchant/train.csv', index_col='card_id', parse_dates=['first_active_month'])
historical_transactions = pd.read_csv('data/elo_merchant/historical_transactions.csv')
print(historical_transactions.head())
