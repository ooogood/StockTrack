from datetime import date, timedelta

def GetToday():
    return date.today().strftime('20%y%m%d')

def GetYesterday():
    yesterday = date.today() - timedelta(days=1)
    return yesterday.strftime('20%y%m%d')

def GetDay(y, m, d):
    # assert we wont look at info before 2000y
    strm = str(m) if m >= 10 else '0'+str(m)
    strd = str(d) if d >= 10 else '0'+str(d)
    return str(y)+strm+strd
