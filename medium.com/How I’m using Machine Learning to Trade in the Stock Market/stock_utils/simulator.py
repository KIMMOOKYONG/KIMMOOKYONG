import numpy as np
import math
import pandas as pd

class simulator:

    """
    시뮬레이션 인스턴스를 생성하면
    파라미터로 전달 받은 초기 투자금, 현재 잔고, 손익, 거래내역 정보를 저장할 변수를 초기화 한다.
    특별이 거래내역정보는 별도의 데이터 프레임으로 저장한다.
    """
    def __init__(self, capital):
        self.capital = capital # 잔고
        self.initial_capital = capital # 초기 투자금
        self.total_gain = 0 # 손익??
        self.buy_orders = {} # 매수 주문
        self.history = [] # 거래 내역 저장?? 히스토리 저장, 아직 정체를 모름??

        # 판다스에 히스토리 저장
        # 하스토리에서 관리하는 칼럼명
        # stock(종목코드, 종목명), buy_price(매수가격), n_shares(거래수량), sell_price(매도가격), net_gain(손익), buy_date(매수일), sell_date(매도일)
        cols = ['stock', 'buy_price', 'n_shares', 'sell_price', 'net_gain', 'buy_date', 'sell_date']
        self.history_df = pd.DataFrame(columns = cols) # cols에서 지정한 칼럼명으로 데이터 프레임 생성
           
    """
    현재 잔고와 매수가를 감안해서 매수를 수행하고, 수행이력을 저장
    """
    def buy(self, stock, buy_price, buy_date):
        """
        function takes buy price and the number of shares and buy the stock
        파라미터로 종목명, 매수가격, 매수일을 전달 받아 주식을 매수하는 함수
        """
        # calculate the procedure
        # 매수 작업 처리에 필요한 연산 작업 수행
        n_shares = self.buy_percentage(buy_price) # 매수 수량 반환
        self.capital = self.capital - buy_price * n_shares # 매수에 따른 잔고 업데이트
        # 매수 내역 저장
        self.buy_orders[stock] = [buy_price, n_shares, buy_price * n_shares, buy_date]

    def sell(self, stock, sell_price, n_shares_sell, sell_date):
        """
        function to sell stock given the stock name and number of shares
        매도할 종목, 수량을 파라미터로 전달 받아 매도한다.
        """
        # 아래의 코드의 구조로는 특정 종목에 대한 매수는 특정 시점에 1 회만하는 구조로 설계되어 있음
        # 복수의 내역을 가지는 구조 설계 변경하는 방안 검토 요망???
        # 종목당 구매 내역을 하나만 가지고 있다. 최종 내역만 보관한다.
        buy_price, n_shares, _, buy_date = self.buy_orders[stock]
        sell_amount = sell_price * (n_shares_sell)

        self.capital = self.capital + sell_amount # 잔고 업데이트

        if (n_shares - n_shares_sell) == 0: #if sold all
            self.history.append([stock, buy_price, n_shares, sell_price, buy_date, sell_date])
            del self.buy_orders[stock]
        else:
            n_shares = n_shares - n_shares_sell
            self.buy_orders[stock][1] = n_shares
            self.buy_orders[stock][2] = buy_price * n_shares

    def buy_percentage(self, buy_price, buy_perc = 1):
        """
        this function determines how much capital to spend on the stock and returns the number of shares
        매수금액 계산
        매수수량 반환
        """
        stock_expenditure = self.capital * buy_perc # 주식 매수에 사용할 지출 금액을 계산
        n_shares = math.floor(stock_expenditure / buy_price) # 지출금액 / 매수가, 정수로 주식주 반환
        return n_shares

    def trailing_stop_loss(self):
        """
        activates a trailing stop loss
        """
        pass
    
    def print_bag(self):
        """
        print current stocks holding
        """
        print ("{:<10} {:<10} {:<10} {:<10}".format('STOCK', 'BUY PRICE', 'SHARES', 'TOTAL VALUE'))
        for key, value in self.buy_orders.items():
            print("{:<10} {:<10} {:<10} {:<10}".format(key, value[0], value[1], value[2]))
        print('\n')  

    def create_summary(self, print_results = False):
        """
        create summary
        """
        if print_results:
            print ("{:<10} {:<10} {:<10} {:<10} {:<10}".format('STOCK', 'BUY PRICE', 'SHARES', 'SELL PRICE', 'NET GAIN'))    
        
        for values in self.history:
            net_gain = (values[3] - values[1]) * values[2]
            self.total_gain += net_gain
            self.history_df = self.history_df.append({'stock': values[0], 'buy_price': values[1], 'n_shares': values[2], 'sell_price': values[3]\
                 ,'net_gain': net_gain, 'buy_date': values[4], 'sell_date': values[5]}, ignore_index = True)
                    
            if print_results:
                print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(values[0], values[1], values[2], values[3], np.round(net_gain, 2)))
            
    def print_summary(self):
        """
        prints the summary of results
        """
        self.create_summary(print_results = True)
        print('\n')
        print(f'Initial Balance: {self.initial_capital:.2f}')
        print(f'Final Balance: {(self.initial_capital + self.total_gain):.2f}')
        print(f'Total gain: {self.total_gain:.2f}')
        print(f'P/L : {(self.total_gain/self.initial_capital)*100:.2f} %')
        print('\n')
