__author__ = 'xierui774'
import pandas as pd
import numpy as np
import Util
import os
from multiprocessing.dummy import Pool as ThreadPool


ma_days = [5,10,20,40,120]
ma_cols = ['MA_close'+str(num) for num in ma_days]+['low']

def is_duo_tou_hui_cai(ma5, ma10, ma20, ma40, ma120, low):
    con = ((ma5>ma10) & (ma10>ma20) & (ma20>ma40)& (ma40>ma120) & (low<ma10))
    return con
def getSingalEntry(code):
    stock = pd.read_csv('d:/Project/Stock/data/'+code,sep='\t').sort_values(by='date')
    for windows_size in ma_days:
        stock['MA_close'+str(windows_size)] = stock['close'].rolling(windows_size).apply(np.mean)
    stock['is_duo_tou_hui_cai'] = stock[ma_cols].apply(lambda x:is_duo_tou_hui_cai(*x),raw=True,axis=1)
    dates = stock.query('is_duo_tou_hui_cai==True')['date'].values

    return (code,dates)

alread_code = [code for code in os.listdir('d:/Project/Stock/data/') if code!='stock_basic.csv']

tuples = []
for code in alread_code:
    res = getSingalEntry(code)
    if len(res[1])>0:
        for dt in res[1]:
            tuples.append(( int(res[0]),dt))
Util.generate_file(tuples,'DUOTOU')
'''
pool = ThreadPool(40)

result = pool.map(getSingalEntry,alread_code)
pool.close()
pool.join()
'''