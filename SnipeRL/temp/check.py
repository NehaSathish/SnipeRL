# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 23:42:20 2021

@author: Akileshvar A Mosi
"""

# from py_code import MAB_models as MAB
from py_code import check_ucb as MAB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

mab = MAB.MultiArmBandit()
mab.prepare_data()
data = mab.get_data()
ucb = mab.upper_confidence_bound(exploration=4853)

time = [i[:19] for i in ucb["time"]]
conf = np.array(ucb["confidence"])
conf_col = [i + "_conf" for i in ucb["stock_dict"].values()]
df = pd.DataFrame(
    data, index=pd.DatetimeIndex(time), columns=ucb["stock_dict"].values()
)
df_ = pd.DataFrame(conf, index=pd.DatetimeIndex(time), columns=conf_col)
df = df.join(df_)
df["return_amount"] = ucb["return_amount"]
df["selected_scrip"] = ucb["selected_scrip"]
display_df = df[['selected_scrip','return_amount']]
# display(display_df.tail(50))


