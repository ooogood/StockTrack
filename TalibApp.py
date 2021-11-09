from talib import abstract
import numpy as np
import pandas as pd
import f_Ut_GetStockHist as GSH

def WhichBBInterval(HistClose, price):
# 0 -> lower -> 1 -> middle -> 2 -> upper -> 3
    bbd = abstract.Function('BBANDS')

    real_data = [float(x) for x in HistClose]
    np_real_data = np.array(real_data)

    upper, middle, lower = bbd( np_real_data,timeperiod=20, nbdevup=2.0, nbdevdn=2.0,matype=2)
    if price <= lower[-1]:
        return 0
    if price <= middle[-1]:
        return 1
    if price <= upper[-1]:
        return 2
    else:
        return 3


#df1 = GSH.GetStockHist('20200501', '2330')
#df2 = GSH.GetStockHist('20200601', '2330')
#result = pd.concat([df1, df2])
#print(WhichBBInterval(result['Close'].values, 280 ))



