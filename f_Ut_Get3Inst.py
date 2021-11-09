import requests
import pandas as pd
from io import StringIO

def GetThreeInstBuy(date):
    # get 3I data
    r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999')

    # form DataFrame with csv
    df = pd.read_csv(StringIO(r.text), header=1, index_col="證券代號").dropna(how='all', axis=1).dropna(how='any')

    # simplify data to 2 columns
    Simplified = pd.DataFrame(df, columns=["證券名稱","三大法人買賣超股數"])
    Simplified.columns = ['StkName', 'ThreeInstBuy']
    Simplified.index.name = 'StkIdx'

    # fix numbers
    TransformThreeInst(Simplified)

    return Simplified

def TransformThreeInst(data):
    for i in data.index:
        try:
            # fix ETF names
            if i[0] == '=':
                newstr = i.replace('=','').replace('"','')
                data.rename({ i : newstr }, axis='index', inplace = True) 
                i = newstr
            # fix numbers
            data.loc[i]['ThreeInstBuy'] = int(data.loc[i]['ThreeInstBuy'].replace(',', ''))
        except:
            data.drop(i, inplace = True)
    return data

def IsThreeInstOverBuy(df, StkIdx):
    try:
        if df.loc[StkIdx]['ThreeInstBuy'] > 0:
            return True
        else:
            return False
    except:
        print('error in G3I with {:s}'.format(StkIdx))
        return False

#df = GetThreeInstBuy('20200609')

