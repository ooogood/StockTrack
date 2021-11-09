import requests
import pandas as pd
from io import StringIO
import os

def GetAllOneDay(datestr):
    # get total data
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')

    # from a DataFrame with csv
    df = pd.read_csv( StringIO(r.text), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1, index_col="證券代號").dropna(how='all', axis=1).dropna(how='any')
    columns = ['StkName', 'TotalAmt', 'TotalTurnover', 'TotalMoney',\
               'Open', 'High', 'Low', 'Close', 'UpDown', 'UpDownMag',\
               'LastBuyPrice','LastBuyAmt','LastSellPrice', 'LastSellAmt', 'PERatio' ]
    df.columns = columns
    df.index.name='StkIdx'
    # fix numbers
    TransformAllOneDay(df)

    return df
    
def TransformAllOneDay(data):
    for index, row in data.iterrows():
        try:
            # fix ETF names
            if index[0] == '=':
                newstr = index.replace('=','').replace('"','')
                data.rename({ index : newstr }, axis='index', inplace = True) 
                index = newstr
            # fix numbers
            data.loc[index, 'TotalAmt'] = int(row['TotalAmt'].replace(',', ''))
            data.loc[index, 'TotalTurnover'] = int(row['TotalTurnover'].replace(',', ''))
            data.loc[index, 'TotalMoney'] = int(row['TotalMoney'].replace(',', ''))
            data.loc[index, 'Open'] = float(row['Open'].replace(',', ''))
            data.loc[index, 'High'] = float(row['High'].replace(',', ''))
            data.loc[index, 'Low'] = float(row['Low'].replace(',', ''))
            data.loc[index, 'Close'] = float(row['Close'].replace(',', ''))
            data.loc[index, 'LastBuyPrice'] = float(row['LastBuyPrice'].replace(',', ''))
            data.loc[index, 'LastBuyAmt'] = float(row['LastBuyAmt'].replace(',', ''))
            data.loc[index, 'LastSellPrice'] = float(row['LastSellPrice'].replace(',', ''))
            data.loc[index, 'LastSellAmt'] = float(row['LastSellAmt'].replace(',', ''))
            data.loc[index, 'PERatio'] = float(row['PERatio'].replace(',', ''))
        except:
            data.drop(index, inplace = True)

    return data

def IsPriceIncrease(df, StkIdx):
    try:
        if df.loc[StkIdx]['UpDown'] != '-':
            return True
        else:
            return False
    except:
        print('error in A1D with {:s}'.format(StkIdx))
        return False

#df = GetAllOneDay('20200610')
#print(print(df.loc['8046']))
