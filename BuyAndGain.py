__author__ = 'xierui774'
import Util
import pandas as pd

dt='2017-03-27'
code='002302'

def buy_and_gain(code,dt,hold_day,gain_percert):
    df = pd.read_csv(Util.base_dir+'data/'+code,sep='\t')
    #print df
    querystr = 'date=="%s"' % dt
    #print querystr
    #print df.query(querystr)
    idx = df.query(querystr).index.values[0]
    res = df.iloc[idx:idx+hold_day+1]
    if len(res)<hold_day+1:
        return 0,0,0
    buy_in_price = res.close.values[0]
    sell_out_price = res.close.values[-1]
    win_sell_out_price = max(res.high.values[1:])
    lose_sell_out_price = min(res.low.values[1:])
    if win_sell_out_price >= buy_in_price*(1+gain_percert):
        return 1,1,gain_percert
    elif lose_sell_out_price <= buy_in_price*(1-gain_percert):
        return 1,-1,-gain_percert
    else:
        return 1,0,(sell_out_price-buy_in_price)/buy_in_price

def period_trans(filename,dt_begin,dt_end):
    i = 0
    res_line = []
    for line in  open(Util.base_dir+filename):
        i+=1
        if i==1:
            continue
        code,dt,name = line.strip().split('\t')
        if dt<dt_begin or dt>dt_end:
            continue
        code = '%06d' % int(code)
        res = buy_and_gain(code,dt,5,0.05)
        res_line.append('\t'.join([code,dt,name,str(res[0]),str(res[1]),str(res[2])]))
    return res_line


if __name__=='__main__':
    filename ='result/Bias_Steady'
    begin_dt = '2015-06-15';
    end_dt = '2017-07-15'
    name = Util.base_dir+filename+'_'+begin_dt+'_'+end_dt+'.evaluate'
    tuples = period_trans(filename,begin_dt,end_dt)
    Util.write_to_file(tuples,name)

