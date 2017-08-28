__author__ = 'xierui774'
import tushare as ts
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt


import tushare as ts
import numpy as np
import pandas as pd
df_07 = ts.get_h_data('000001',start='2007-10-01',end='2009-10-01',index=True)
df_15 = ts.get_h_data('000001',start='2014-10-01',end='2017-04-27',index=True)
df = df_07['close'].sort_index()
df2 = df_15['close'].sort_index()
idx = np.argmax(df.values)
idx2 = np.argmax(df2.values)
df_new = df2.values[idx2-idx:]
df = pd.DataFrame(df)
df['new_close']=np.nan
df.ix[:len(df_new),'new_close']=df_new
df.plot()
plt.show()