# -*- coding: utf-8 -*-
"""
Created on Fri May 14 11:31:01 2021

@author: Akileshvar A Mosi
"""

from py_code import check_ucb as MAB
import json
from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed

def return_roi(val):
    return mab.upper_confidence_bound(exploration=val)["roi"]

with open('bruteforce_env/all_order.json') as file:
    all_order = json.load(file)
    
with open('bruteforce_env/brute_checkpoint.json') as file:
    checkpoint = json.load(file)
    
iteration = checkpoint[-1]['iteration']
num_cores = multiprocessing.cpu_count()

for i in tqdm(range(iteration,int(len(all_order)))):
    mab = MAB.MultiArmBandit()
    mab.set_filepath('bruteforce_env/data/')
    mab.prepare_data(file_order=all_order[i])
    data = mab.get_data()
    inputs = (range(data.shape[0]))
    processed_list = Parallel(n_jobs=num_cores)(delayed(return_roi)(i)
                                                for i in inputs)
    
    savejson = dict(
        iteration=i+1,
        max_roi=max(processed_list),
        magic_number=processed_list.index(max(processed_list)),
        )
    
    checkpoint.append(savejson)
    with open('bruteforce_env/brute_checkpoint.json','w') as file:
        json.dump(checkpoint,file,indent=4)
