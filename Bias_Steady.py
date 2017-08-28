__author__ = 'xierui774'
import pandas as pd
import numpy as np
import Util
import os
day_before = 2
cols = {
    'close':[1,2,3,4,5],
    'open':[1,2,3,4]
}

def is_single_bottom(close_period, close, low_steady, high_steady):
    if close_period > close * 1.20 and low_steady > close*0.97 and high_steady < close * 1.03:
        return 1
    else:
        return 0


def getSingalEntry(code, period,steady_period):
    stock = pd.read_csv('d:/Project/Stock/data/'+code,sep='\t').sort_values(by='date')
    cols_new = ['MA'+str(period)+'_close','close','Low_'+str(steady_period),'High_'+str(steady_period) ]
    stock['MA'+str(period)+'_close'] = stock['close'].rolling(period).apply(np.mean)
    stock['High_'+str(steady_period)] = stock['high'].rolling(steady_period).apply(np.max)
    stock['Low_'+str(steady_period)] = stock['low'].rolling(steady_period).apply(np.min)
    stock['is_single_bottom'] = stock[cols_new].apply(lambda x:is_single_bottom(*x),raw=True,axis=1)
    dates = stock.query('is_single_bottom==1')['date'].values
    return (code,dates)

alread_code = [code for code in os.listdir('d:/Project/Stock/data/') if code!='stock_basic.csv'and code!='stock_concept.csv']

tuples = []
for code in alread_code[:]:
    res = getSingalEntry(code,20, 5)
    if len(res[1])>0:
        for dt in res[1]:
            tuples.append(( int(res[0]),dt))
Util.generate_file(tuples,'Bias_Steady')