__author__ = 'xierui774'
import pandas as pd
import numpy as np
import Util
import os
from multiprocessing.dummy import Pool as ThreadPool


windows_size = 20

def getSingalEntry(code):
    stock = pd.read_csv('d:/Project/Stock/data/'+code,sep='\t').sort_values(by='date')
    stock['MA'+str(windows_size)] = stock['close'].rolling(windows_size).apply(np.mean)
    stock['UNDER_MA'+str(windows_size)] = stock[['close','MA'+str(windows_size)]].apply(lambda x: 1 if x[0]<x[1] else 0,raw=True,axis=1)
    stock['UNDER_MA'+str(windows_size)+'_LONG_ENOUGH'] = stock['UNDER_MA'+str(windows_size)].rolling(2*windows_size).apply(lambda x : sum(x)>=2*windows_size and x[-1]==1)
    dates = stock.query('UNDER_MA'+str(windows_size) +'_LONG_ENOUGH==1')['date'].values

    return (code,dates)

alread_code = [code for code in os.listdir('d:/Project/Stock/data/') if code!='stock_basic.csv']

tuples = []
for code in alread_code:
    res = getSingalEntry(code)
    if len(res[1])>0:
        for dt in res[1]:
            tuples.append(( int(res[0]),dt))
Util.generate_file(tuples,'Long_Below_MA_Bound')
'''
pool = ThreadPool(40)

result = pool.map(getSingalEntry,alread_code)
pool.close()
pool.join()
'''