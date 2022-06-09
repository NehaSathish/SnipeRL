from os import walk
from time import sleep
import yfinance as yf
import pandas as pd

data_filepath = 'IntradayDatasetPrep/15mins_data/'
_, _, filenames = next(walk(data_filepath))
stock_names = [i[:-4]+".NS" for i in filenames ]

for i in filenames:
    data = pd.read_csv(data_filepath+i)
    data_dup = data.drop('Unnamed: 0',axis=1)
    data_dup.to_csv(data_filepath+i,index=False)