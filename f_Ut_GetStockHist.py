import numpy as np
import requests
import pandas as pd

def GetStockHist(date, StkIdx):
    # get stock data for a month
    r = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=' + date + '&stockNo=' + StkIdx )
    data = pd.DataFrame(r.json()['data'])
    data.columns = ['Date', 'Shares', 'Amount', 'Open', 'High', 'Low', 'Close', 'Change', 'Turnover']
                   #"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數" 
    for i in data.index:
        TransformStockHist(data.loc[i])

    # add one line as stock index note
    data['StkIdx'] = StkIdx
    return data

def TransformStockHist(row):
    row['Date'] = TransformDate(row['Date'])
    row['Shares'] = int(row['Shares'].replace(',', ''))
    row['Amount'] = int(row['Amount'].replace(',', ''))
    row['Open'] = float(row['Open'].replace(',', ''))
    row['High'] = float(row['High'].replace(',', ''))
    row['Low'] = float(row['Low'].replace(',', ''))
    row['Close'] = float(row['Close'].replace(',', ''))
    row['Change'] = float(0.0 if row['Change'].replace(',', '') == 'X0.00' else row['Change'].replace(',', '')) 
    row['Turnover'] = int(row['Turnover'].replace(',', ''))
    return

def TransformDate(date):
    y, m, d = date.split('/')
    return str(int(y)+1911)+ m + d

#df = GetStockHist('20200601', '2330')
#print(df)
#print(type(df))