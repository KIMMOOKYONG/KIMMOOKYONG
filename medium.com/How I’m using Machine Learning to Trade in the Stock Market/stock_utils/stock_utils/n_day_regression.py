import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

import requests
import json
import time
from pandas import DataFrame
from datetime import datetime
import datetime as dt
import math

"""
주가 데이터(OHLC) 정규화
"""
def normalized_values(high, low, close):
    """
    normalize the price between 0 and 1.
    """
    #epsilon to avoid deletion by 0
    epsilon = 10e-10
    
    #subtract the lows
    high = high - low
    close = close - low
    return close / (high + epsilon)

def get_data(ticker, start_date = None, end_date = None, n = 10):

    # enter url
    url = f"https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day"

    # request
    results = requests.post(url)
    data = results.text.replace("'",  '"').strip()
    data = json.loads(data)

    # change the data from ms to datetime format
    data = pd.DataFrame(data[1:], columns=data[0])
    data = data.reset_index()
    data["날짜"] = pd.to_datetime(data["날짜"])

    data = data[["날짜","시가", "고가", "저가", "종가", "거래량"]]
    data.columns = ["date", "open", "high", "low", "close", "volume"]
    data = data.set_index("date")
    data = data.dropna()
    data.loc[:,["open", "high", "low", "close", "volume"]] = data.loc[:,["open", "high", "low", "close", "volume"]].astype(int)
    data = data.loc[:,["open", "high", "low", "close", "volume"]]

    # add the noramlzied value function and create a new column
    data['normalized_value'] = data.apply(lambda x: normalized_values(x.high, x.low, x.close), axis = 1)
    
    #column with local minima and maxima
    data['loc_min'] = data.iloc[argrelextrema(data.close.values, np.less_equal, order = n)[0]]['close']
    data['loc_max'] = data.iloc[argrelextrema(data.close.values, np.greater_equal, order = n)[0]]['close']

    #idx with mins and max
    idx_with_mins = np.where(data['loc_min'] > 0)[0]
    idx_with_maxs = np.where(data['loc_max'] > 0)[0]
    
    return data, idx_with_mins, idx_with_maxs

"""
선형회귀를 통한 기울기를 반환하는 함수
x,y: 2차원 배열 값
"""
def linear_regression(x, y):
    """
    performs linear regression given x and y. outputs regression coefficient
    """
    #fit linear regression
    lr = LinearRegression()
    lr.fit(x, y)
    
    return lr.coef_[0][0]

"""
n 기간 동안의 선형회귀(기울기) 계산
"""
def n_day_regression(n, df, idxs):
    """
    n day regression(기울기 계산)
    """
    #variable
    _varname_ = f'{n}_reg'
    df[_varname_] = np.nan

    for idx in idxs:
        if idx > n:
            
            y = df['close'][idx - n: idx].to_numpy()
            x = np.arange(0, n)
            # reshape
            y = y.reshape(y.shape[0], 1)
            x = x.reshape(x.shape[0], 1)
            # calculate regression coefficient
            # 기울기 계산
            coef = linear_regression(x, y)
            df.loc[idx, _varname_] = coef #add the new value
            
    return df


if __name__ == '__main__':
    ticker = '001440'
    st = '20210101'
    ed = '20220404'
    data = get_data(ticker, st, ed)

    n_day_regression(n, df, idxs)


n_day_regression(3, data, list(idxs_with_mins) + list(idxs_with_maxs))
