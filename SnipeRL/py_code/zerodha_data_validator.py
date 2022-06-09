# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:34:11 2021

@author: Akileshvar A Mosi
"""

from os import walk
import pandas as pd

data_filepath = "IntradayDatasetPrep/5mins_data/"
_, _, filenames = next(walk(data_filepath))


df_list = list()
for i in filenames:
    df_list.append(pd.read_csv(data_filepath + i))

'''
#RUN FIRST TIME

for i, k in zip(df_list, filenames):
    i.drop(["SYMBOL", "Date", "TIME1"], axis=1, inplace=True)
    i.rename(
        {"VOLUME": "Volume", "TIME": "Time", "CLOSE": "Close"}, axis=1, inplace=True
    )
    i.reset_index(drop=True, inplace=True)
    i = i.drop_duplicates()
    i.to_csv(data_filepath + k,index=None)

'''

'''
#Find the drop_val and drop_index and run this cell

drop_val = '2020-04-27 15:30:00'
drop_index = 79485

for i in filenames:
    temp = (pd.read_csv(data_filepath+i))
    if (temp.iloc[drop_index]['Time']) == drop_val:
        temp = temp.drop(drop_index)
        temp.to_csv(data_filepath+i,index=None)
'''
