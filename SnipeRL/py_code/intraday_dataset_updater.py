
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:35:31 2021

@author: Akileshvar A Mosi
"""

from os import walk
import yfinance as yf
import pandas as pd

data_filepath = 'IntradayDatasetPrep/15mins_data/'

df_list = list()
_, _, filenames = next(walk(data_filepath))
stock_names = [i[:-4]+".NS" for i in filenames ]

for i in filenames:
    df_list.append(pd.read_csv(data_filepath + i))

final = list()
for i,j,k in zip(df_list,stock_names,filenames):
    # new_data = yf.download(tickers=j,period='1d',interval='60m')
    # new_data.drop(['Adj Close'],axis=1,inplace=True)
    # new_data.reset_index(inplace=True)
    # new_data.rename({'Datetime':'Time'},axis=1,inplace=True)
    # new_data.drop(new_data.tail(1).index,inplace=True)
    
    i.drop(['SYMBOL',"Date",'TIME1'],axis=1,inplace=True)
    i.rename({'VOLUME':'Volume','TIME':'Time','CLOSE':'Close'},axis=1,inplace=True)
    
    # i = i.append(new_data)
    i.reset_index(drop=True,inplace=True)  
    i = i.drop_duplicates()
    i.to_csv(data_filepath+k)