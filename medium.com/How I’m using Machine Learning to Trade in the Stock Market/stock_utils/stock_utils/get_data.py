"""
주가 데이터 다운로드 및 주가 데이터 정규화
주가 데이터를 다운로드 받아서,
가격 OHLC를 하나의 정수값으로 정규화하고,
가격의 변곡점(local 저가, local 고가)를 추출해서 반환하는 함수
"""
def get_data(ticker, start_date = None, end_date = None, n = 10):
    """
    주가 데이터 다운로드
    """
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

    """
    주가 데이터 정규화
    """
    # add the noramlzied value function and create a new column
    data['normalized_value'] = data.apply(lambda x: normalized_values(x.high, x.low, x.close), axis = 1)
    
    # column with local minima and maxima
    # 1D numpy 배열에서 Numpy를 사용하여 로컬 최대 값 / 최소값 찾기
    # 기준일 기준으로 전후의 10일 종가를 비교해서 로컬 최대, 최소값의 index를 반환한다. n = 10
    # 가격의 전환점을 발견, find turning points
    data['loc_min'] = data.iloc[argrelextrema(data.close.values, np.less_equal, order = n)[0]]['close']
    data['loc_max'] = data.iloc[argrelextrema(data.close.values, np.greater_equal, order = n)[0]]['close']

    # idx with mins and max
    # [0]을 하는 이유는 튜플에서 배열값 추출, (배열값,) -> 배열값
    # 가격의 변곡점(turning points 추출)
    idx_with_mins = np.where(data['loc_min'] > 0)[0]
    idx_with_maxs = np.where(data['loc_max'] > 0)[0]
    
    return data, idx_with_mins, idx_with_maxs

if __name__ == 'main':
    ticker = '001440'
    data, idx_with_mins, idx_with_maxs = get_data(ticker, '20210101', '20220404')
