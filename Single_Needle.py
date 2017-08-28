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

def is_single_bottom(open,close,low,close1,close2,close3,close4,close5,open1,open2,open3,open4):
    con1 =  (close<open) & (close1<open1) & (close2<open2) & (close3<open3) & (close4<open4)
    con2 = (close<close1) & (close1<close2) &(close2<close3) &(close3<close4) &(close4<close5)
    con3 =  (close/low>1.06)
    con4 =   ((close-close1)/close1 + (close1-close2)/close2 + (close2-close3)/close3 + (close3-close4)/close4 + (close4-close5)/close5)<(-0.025*5)
    if  con1 & con2 & con3 & con4:
        return 1
    else:
        return 0


def getSingalEntry(code):
    stock = pd.read_csv('d:/Project/Stock/data/'+code,sep='\t').sort_values(by='date')
    cols_new = ['open','close','low']
    for col in cols.keys():
        for i in cols[col]:
            cols_new.append(col+str(i))
            stock[col+str(i)] = stock[col].shift((i))
    stock['is_single_bottom'] = stock[cols_new].apply(lambda x:is_single_bottom(*x),raw=True,axis=1)
    dates = stock.query('is_single_bottom==1')['date'].values
    return (code,dates)

alread_code = [code for code in os.listdir('d:/Project/Stock/data/') if code!='stock_basic.csv'and code!='stock_concept.csv']

tuples = []
for code in alread_code[:]:
    res = getSingalEntry(code)
    if len(res[1])>0:
        for dt in res[1]:
            tuples.append(( int(res[0]),dt))
Util.generate_file(tuples,'Singe_Needle')