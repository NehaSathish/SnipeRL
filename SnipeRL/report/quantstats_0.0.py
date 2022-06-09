# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 14:58:30 2021

@author: Akileshvar A Mosi
"""

import quantstats as qs
from RLmethods.check_ucb import MultiArmBandit
from tqdm import tqdm
import pandas as pd
from dateutil import parser
import numpy as np

report = dict()
magic_number = 4852

mab = MultiArmBandit()
mab.prepare_data()
data = mab.get_data()
ucb = mab.UpperConfidenceBound(magic_number)

def report (filename = ''):

    new_time = [(parser.parse(i).replace(tzinfo=None)) for i in tqdm(mab.date_time)]
    return_amount = ucb["return_amount"]
    day_time = [parser.parse((i.date()).ctime()) for i in new_time[::25]]
    day_return = return_amount[::25]
    return_series = pd.Series(day_return,index=day_time,name='return_series')
    day_percent_qs = qs.utils.to_returns(return_series)
    qs.reports.html(day_percent_qs,output=filename)