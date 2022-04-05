import requests
import json
import time
import math
from datetime import datetime
import datetime as dt
import numpy as np
import pandas as pd

#----------------------------
# 네이버 금융에서 주가 데이터 다운로드 받기
# ticker: 종목코드
# start: 시작일
# end: 종료일
#----------------------------
def s_download(ticker, start, end, isWrite=False):
    time.sleep(0.2)
    url = f"https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={start}&endTime={end}&timeframe=day"
    result = requests.post(url)

    data1 = result.text.replace("'",  '"').strip()
    data1 = json.loads(data1)

    data2 = pd.DataFrame(data1[1:], columns=data1[0])
    data2 = data2.reset_index()
    data2["날짜"] = pd.to_datetime(data2["날짜"])

    df = data2[["날짜","시가", "고가", "저가", "종가", "거래량"]].copy()
    df.columns = ["date", "open", "high", "low", "close", "volume"]
    df = df.set_index("date")
    df = df.dropna()
    df.loc[:,["open", "high", "low", "close", "volume"]] = df.loc[:,["open", "high", "low", "close", "volume"]].astype(int)
    df = df.loc[:,["open", "high", "low", "close", "volume"]]

    if isWrite:
        df.to_csv(f'{ticker}.csv')

    return df

# 데이터 저장: s_download('001440', '20210101', '20220405', True)
