__author__ = 'xierui774'
import pandas as pd
import os
import numpy as np
import Util
base_dir = Util.base_dir

def similarity(code, windows=10,column='close',max_num=10):
    df_code = pd.read_csv(base_dir+'data/'+code,sep='\t')
    value_list = df_code.tail(n=windows)[column].values
    def corr(x):
        return np.corrcoef(x,value_list)[0,1]
    alread_code = os.listdir(base_dir+'data/')
    df_res_all = pd.DataFrame([[-1,-1]])
    df_res_all.columns = [column,'code']
    for i,y_code in enumerate(alread_code):
        if i%50==0:
            print y_code
        if y_code!=code and y_code.endswith('.csv')==False:
            df_y_code = pd.read_csv(base_dir+'data/'+y_code,sep='\t').set_index('date')[column]
            df_res = df_y_code.rolling(windows).apply(corr)
            df_res = pd.DataFrame(df_res)
            df_res['code']=y_code
            df_res = df_res.sort_values(by=column, ascending=False).head(n=max_num)
            df_res_all = df_res_all.append(df_res)
    return df_res_all.sort_values(by=column,ascending=False).head(n=max_num), value_list
df_res, value_list = similarity('000002')

