import pandas as pd
import requests
import os

def GetInstPrice(targets):
    # form stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 
    # request
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    data = requests.get(url).json()
    # get and rename useful columns
    columns = ['c','b','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['StkIdx','NowBuyPrice','TotalAmt','Open','High','Low','YesClose']
             #['股票代碼','當盤買進價','累積成交量(張)','開盤價','最高價','最低價','昨收價']
    # use nowbuyprice as nowprice because 'z' might be '-'(no value)
    df.set_index('StkIdx', inplace=True)

    # fix numbers
    for x in df.index:
        try:
            df.loc[x, ['TotalAmt','Open','High','Low','YesClose']] = \
             df.loc[x, ['TotalAmt','Open','High','Low','YesClose']].astype(float)
            df.loc[x, 'NowBuyPrice'] = float( df.loc[x, 'NowBuyPrice'].split('_')[0] )
        except:
            df.drop( x, inplace = True)

    return df

def IsPriceIncrease(df, StkIdx):
    try:
        if df.loc[StkIdx]['NowBuyPrice'] > df.loc[StkIdx]['YesClose']:
            return True
        else:
            return False
    except:
        print('error in GIP with {:s}'.format(StkIdx))
        return False

#df = GetInstPrice(['6216'])
#print(df)
