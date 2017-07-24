__author__ = 'xierui774'
import pandas as pd
import numpy as np
import os
base_dir = 'd:/Project/Stock/StockTrading/'

def generate_file(tuples, filename, base_dir=base_dir):
    df = pd.read_csv(base_dir+'data/stock_basic.csv',sep='\t')[['code','name']]
    df_res = pd.DataFrame(tuples)
    df_res.columns = ['code','dt']
    df = pd.merge(df_res,df,on='code')
    df = df.sort_values(by='dt',ascending=False)
    df.to_csv(base_dir+'result/'+filename, sep='\t',index=False)

def visual_similarity(value_list, res, windows=20):
    ys = [value_list]
    for i,row in enumerate(res.values):
        dt = res.index.values[i]
        code = row[1]
        df_code = pd.read_csv(base_dir+'data/'+code,sep='\t')
        df_code = df_code.set_index('date')['close']
        idx = df_code.index.get_loc(dt)
        y = df_code.iloc[idx-windows+1:idx+windows].values
        t = value_list[0]/y[0]
        y = np.array([yi*t for yi in y])
        ys.append(y)
    return ys

def delete_files_in_dir(dir):
    for filename in os.listdir(dir):
        os.remove(dir+filename)
#t = visual_similarity(value_list,df_res)
#pd.DataFrame(t).T.plot()

def write_to_file(lines,name):
    f = open(name,'w')
    for line in lines:
        f.write(line+'\n')
    f.close()


if '__main__'==__name__:
    delete_files_in_dir(base_dir+'data/')