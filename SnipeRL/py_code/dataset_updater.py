# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 23:07:46 2021

@author: Akileshvar A Mosi
"""

import pandas as pd
import numpy as np

def update_dataset( prev_date, curr_date):

    dataset_path = 'StockWise/DatasetTop10_feb2016/data.csv'
    data_df = pd.read_csv(dataset_path)
    data = np.array(data_df)
    stock_names = list(data_df.columns)
    prev_df = pd.read_csv("StockWise/1Apr2016_22Jan2021/" + prev_date + "_NSE.csv")
    curr_df = pd.read_csv("StockWise/1Apr2016_22Jan2021/" + curr_date + "_NSE.csv")
    prev_values = [float(prev_df.query("SYMBOL == @i")["CLOSE"]) for i in stock_names]
    curr_values = [float(curr_df.query("SYMBOL == @i")['CLOSE']) for i in stock_names]
    packed_values = zip(prev_values, curr_values)
    perc = [((curr - prev) / prev) * 100 for prev, curr in packed_values]
    perc_array = (np.array(perc))
    perc_array = np.reshape(perc_array,(1,data.shape[1]))
    updated_data = np.append(data, perc_array, axis=0)
    updated_data_df = pd.DataFrame(updated_data, columns=stock_names)
    updated_data_df.to_csv(dataset_path, index=False)
    return

# print('Date Format : YYYYMMDD')
# prev_date = input("Enter the Previous Trading Date : ")
# curr_date = input("Enter the Current Trading Date : ")
# update_dataset(prev_date,curr_date)

update_dataset('20210203','20210204')