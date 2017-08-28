__author__ = 'xierui774'
import pandas as pd
import numpy as np
import Util
import os
day_before = 2
cols = ['close','high','low','open']

def is_red_three_solider(close, high, low, open, close1, close2, high1, high2, low1, low2, open1, open2):
    con1 =  (close>open) & (close1>open1) & (close2>open2)
    con2 = (close>close1) & (close1>close2)
    con3 =  (open < close1) & (open > open1) & (open1 < close2) & (open1 > open2)
    #con3 =  (open > open1)  & (open1 > open2)
    con4 =  (((high-close) < (close-open) *0.25)) & (((high1-close1) < (close1-open1) *0.25)) & (((high2-close2) < (close2-open2) *0.25))
    con5 =  (((open-low) < (close-open) *0.25)) & (((open1-low1) < (close1-open1) *0.25)) & (((open2-low2) < (close2-open2) *0.25))

    if  con1 & con2 & con3 & con4:
        return 1
    else:
        return 0


def getSingalEntry(code):
    stock = pd.read_csv('d:/Project/Stock/data/'+code,sep='\t').sort_values(by='date')
    cols_new = cols[:]
    for col in cols:
        for i in range(day_before):
            cols_new.append(col+str(i+1))
            stock[col+str(i+1)] = stock[col].shift((i+1))
    #print cols_new
    stock['is_red_three_soldier'] = stock[cols_new].apply(lambda x:is_red_three_solider(*x),raw=True,axis=1)
    dates = stock.query('is_red_three_soldier==1')['date'].values
    return (code,dates)

alread_code = [code for code in os.listdir('d:/Project/Stock/data/') if code!='stock_basic.csv'and code!='stock_concept.csv']

tuples = []
for code in alread_code:
    res = getSingalEntry(code)
    if len(res[1])>0:
        for dt in res[1]:
            tuples.append(( int(res[0]),dt))
Util.generate_file(tuples,'RED_Three_Soldier_Not_Jump')