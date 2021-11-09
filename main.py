# import talib 
import time
import pandas as pd
import f_Ut_Get3Inst as G3I
import f_Ut_GetInstPrice as GIP
import f_Ut_AllOneDay as A1D
import f_Ut_GetStockHist as GSH
import f_Ut_GetTime as Timestr
import TalibApp as TA
import os
import csv

y = 2020
m = 6
d = 15
# Get date string
#ydate = Timestr.GetYesterday()
ydate = Timestr.GetDay(y, m, d)
lmdate = Timestr.GetDay( y, m-1, d )

# Get yesterday's 3 institutional investor info
Yes3InstInfo = G3I.GetThreeInstBuy(ydate)
# Get yesterday's Stock Basic
Yesterday = A1D.GetAllOneDay(ydate)

# iterate through all stock index and choose winner
# 50 stocks at a time, prevanting blocked by twse.com
winner = []
winprice = []
start = 0
end = 0
step = 50
bBreak = False
TotalStock = len(Yes3InstInfo.index)
while end < TotalStock:
    # iteration: advance end
    end = end + step
    if end >= TotalStock: end = TotalStock

    # Get instant price
    InstPrice = GIP.GetInstPrice( Yes3InstInfo.index[start:end] )

    # check each stock x in interval
    for x in Yes3InstInfo.index[start:end]:
        try:
            # condition 1: if 3I over buy yesterday?
            if G3I.IsThreeInstOverBuy(Yes3InstInfo, x) == False:
                # since Yes3InstInfo is arranged by the order of 3I buy amount
                # rest of the stock will not pass this
                # not continue but break
                bBreak = True
                break

            # condition 2: if price increase yesterday?
            if A1D.IsPriceIncrease(Yesterday, x) == False:
                continue

            # condition 3: if price increase today?
            if GIP.IsPriceIncrease(InstPrice, x) == False:
                continue

            # condition 4: if today's amount bigger than yesterday*0.8 ?
            if InstPrice.loc[x]['TotalAmt'] * 1000 < Yesterday.loc[x]['TotalAmt'] * 1.1:
                continue

            # condition 5: if total amount > 500?
            if InstPrice.loc[x]['TotalAmt'] < 500:
                continue
        
            # we got a winner!
            print('=====winner=====')
            print(x)
            print('now price: {:f}'.format(InstPrice.loc[x]['NowBuyPrice']))
            print('================')
            winner.append(x)
            winprice.append(InstPrice.loc[x]['NowBuyPrice'])
        except:
            print('skip:')
            print(x)
            continue

    # iteration: advance start
    print(end)
    start = end
    if bBreak == True: break
    time.sleep(5)

# print winner's name
for i in range(len(winner)):
    df1 = GSH.GetStockHist( lmdate, winner[i] )
    time.sleep(5)
    df2 = GSH.GetStockHist( ydate, winner[i] )
    result = pd.concat([df1, df2])
    print('{:s} {:s} {:f} {:d}'.format(winner[i], \
                                       Yes3InstInfo.loc[winner[i]]['StkName'],\
                                       winprice[i],\
                                       TA.WhichBBInterval(result['Close'].values, winprice[i] )))
    time.sleep(5)

# write today's winner into csv
with open( Timestr.GetToday() + '.csv', 'w', newline= '') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(winner)
