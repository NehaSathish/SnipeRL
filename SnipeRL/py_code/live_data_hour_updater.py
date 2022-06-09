# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:03:26 2021

@author: Akileshvar A Mosi
"""

from os import walk
from time import sleep
import yfinance as yf

data_filepath = 'data/15mins_data/'
_, _, filenames = next(walk(data_filepath))
stock_names = [i[:-4]+".NS" for i in filenames ]

final = []
# while True:
for i,j in zip(stock_names,filenames):
    new_data = yf.download(tickers=i,period='1d',interval='15m')
    new_data.drop(['Adj Close'],axis=1,inplace=True)
    # new_data.reset_index(inplace=True)
    new_data.rename({'Datetime':'Time'},axis=1,inplace=True)
    # new_data = (new_data.tail(5))
    
    new_data.head(25).to_csv(data_filepath+j,mode='a',header=False)
    # final.append(new_data)