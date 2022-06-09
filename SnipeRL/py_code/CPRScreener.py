# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 19:43:17 2021

@author: Akileshvar A Mosi
"""

import pandas as pd
import numpy as np


def csv2list(data):
    return [(i[4:]).replace("_", "&") for i in list(data.columns)]


filepath = "data/bhavcopy/20210506_NSE.csv"

data = (pd.read_csv(filepath)).query('SERIES == "EQ"')
ohlc_arr = np.array(data[["OPEN", "HIGH", "LOW", "CLOSE"]])
scrip = list(data["SYMBOL"])

pivot = (ohlc_arr[:, 1] + ohlc_arr[:, 2] + ohlc_arr[:, 3]) / 3
x1 = (ohlc_arr[:, 1] + ohlc_arr[:, 2]) / 2
x2 = (pivot - x1) + pivot
resistance = (pivot * 2) - ohlc_arr[:, 2]
support = (pivot * 2) - ohlc_arr[:, 1]
cpr_perc = abs((pivot - x1) * 100 / pivot)
rs_perc = abs((resistance - support) * 100 / support)

fno_list = csv2list(pd.read_csv("data/_ FNO Watchlist _.txt"))
pf_list = csv2list(pd.read_csv("data/_ PORTFOLIO _.txt"))

N = 10
result = pd.DataFrame(dict(SYMBOL=scrip, cpr_perc=cpr_perc, rs_perc=rs_perc))
fno_cpr = (result.loc[result["SYMBOL"].isin(fno_list)]).sort_values(by=["cpr_perc"])
print("FNO\n\nPIVOT_PERCENTAGE\n\n", fno_cpr.head(N)["SYMBOL"])

fno_rs = (result.loc[result["SYMBOL"].isin(fno_list)]).sort_values(by=["rs_perc"])
print("\n\nRS_PERCENTAGE\n\n", fno_rs.head(N)["SYMBOL"])

pf = (result.loc[result["SYMBOL"].isin(pf_list)]).sort_values(by=["cpr_perc"])
print("\n\nPORTFOLIO\n\nPIVOT_PERCENTAGE\n\n", pf.head(N)["SYMBOL"])

pf = (result.loc[result["SYMBOL"].isin(pf_list)]).sort_values(by=["rs_perc"])
print("\n\nRS_PERCENTAGE\n\n", pf.head(N)["SYMBOL"])
