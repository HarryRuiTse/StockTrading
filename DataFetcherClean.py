__author__ = 'xierui774'

import pandas as pd
import numpy as np
import tushare as ts
import os
import urllib2
import datetime
import Util
from multiprocessing.dummy import Pool as ThreadPool

base_dir = Util.base_dir


if os.path.exists(base_dir+'data/stock_basic.csv'):
    df = pd.read_csv(base_dir+'data/stock_basic.csv',sep='\t')
    df = df.set_index('code')
    #t = pd.read_csv(base_dir+'data/stock_concept.csv',sep='\t',encoding='utf-8')
else:
    df = ts.get_stock_basics()
    df.to_csv(base_dir+'data/stock_basic.csv',sep='\t')
    #t = ts.get_concept_classified()
    #t.to_csv(base_dir+'data/stock_concept.csv',sep='\t',index=False,encoding='utf-8')
print df.head()
codes = df.index.values
alread_code = os.listdir(base_dir+'data/')



def gen_get_single(already_codes):
    def get_single(code):
        for i in [0,1,2]:
            try:
                if type(code)==type(1) or type(code)==type(np.array([1])[0]):
                    code = '%06d' % code
                if code not in alread_code:
                    print type(code)
                    df_code = ts.get_k_data(code)
                    #print df_code
                    print type(df_code)
                    if type(df_code)!=type(None) and len(df_code)>0:
                        df_code.to_csv(base_dir+'data/'+code , sep='\t',index=False)
                break
            except urllib2.URLError:
                continue
            except IndexError:
                break
        return 1
    return get_single


def get_all(codes,f):
    print type(codes)
    pool = ThreadPool(40)
    pool.map(f,codes)
    pool.close()
    pool.join()

def get_all_serial(codes,f):
    for code in codes:
        f(code)

def inc_get_single(code):
    if os.path.exists(base_dir+'data/'+code):
        df_code = pd.read_csv(base_dir+'data/'+code,sep='\t')
        del df_code['Unnamed: 0']
        today_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
        for i in [0,1,2]:
            try:
                df_code_new = ts.get_k_data(code,start=today_str)
                break
            except urllib2.URLError:
                    continue
        df_code = df_code.append(df_code_new)
        df_code = df_code.drop_duplicates()
        df_code.to_csv(base_dir+'data/'+code+'_new',sep='\t',index=False)

#Util.delete_files_in_dir(Util.base_dir+'data/')
gs = gen_get_single(alread_code)
#get_all_serial(list(codes),gs)
get_all(list(codes),gs)
#geget_all_serial(list(codes),gs)t_all(codes,inc_get_single)


