# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 21:08:20 2021

@author: Akileshvar A Mosi
"""

from RLmethods.MAB_models import MultiArmBandit
import pandas as pd
import numpy as np
from os import walk
import yfinance as yf
import json
import math


def update_average(old_avg, stock_count, new_reward):
    return ((old_avg * (stock_count - 1)) + new_reward) / stock_count


def update_confidence(average, stock_count, pull_count):
    if stock_count == 0:
        return 0
    return average + np.sqrt((2 * math.log(pull_count)) / stock_count)


data_filepath = "IntradayDatasetPrep/15mins_data/"
_, _, filenames = next(walk(data_filepath))
stock_names = [i[:-4] + ".NS" for i in filenames]

final = []
for i, j in zip(stock_names, filenames):
    new_data = yf.download(tickers=i, period="8d", interval="15m")
    new_data.drop(["Adj Close"], axis=1, inplace=True)
    new_data.rename({"Datetime": "Time"}, axis=1, inplace=True)
    final.append(new_data.iloc[0]["Close"])

report = dict()
mab = MultiArmBandit()
mab.prepare_data()
data = mab.get_data()
ucb = mab.upper_confidence_bound()

with open("RLmethods/data/checkpoint.json") as file:
    checkpoint = json.load(file)

last_close = checkpoint["last_close"]

perc_change = list()
for curr, prev in zip(final, last_close):
    perc_change.append(((curr - prev) / prev) * 100)


arm = checkpoint["confidence"].index(max(checkpoint["confidence"]))
checkpoint["stock_count"][arm] += 1
rew = perc_change[arm]
checkpoint["average_reward"][arm] = update_average(
    checkpoint["average_reward"][arm], checkpoint["stock_count"][arm], rew
)
for hand_ind in range(10):
    checkpoint["confidence"][hand_ind] = update_confidence(
        checkpoint["average_reward"][hand_ind],
        checkpoint["stock_count"][hand_ind],
        checkpoint["iteration"] + 1,
    )
