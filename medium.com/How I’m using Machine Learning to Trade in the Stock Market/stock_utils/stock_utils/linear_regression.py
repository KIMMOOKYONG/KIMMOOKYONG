"""
### 선형 회귀란 무엇인가?
머신 러닝의 가장 큰 목적은 실제 데이터를 바탕으로 모델을 생성해서 만약 다른 입력 값을 넣었을 때
발생할 아웃풋을 예측하는 데에 있다.

이때 우리가 찾아낼 수 있는 가장 직관적이고 간단한 모델은 선(line)이다.
그래서 데이터를 놓고 그걸 가장 잘 설명할 수 있는 선을 찾는 분석하는 방법을 
선형 회귀(Linear Regression) 분석이라 부른다.

결국 선형 회귀 모델의 목표는 모든 데이터로부터 나타나는 오차의 평균을 최소화할 수 있는
최적의 기울기와 절편을 찾는 거다.

### 경사하강법(Gradient Descent)
파라미터를 임의의 값으로 정한 다음에 조금씩 변화시켜가며 손실을 점점 줄여가는 방법(편미분, 순간변화율)으로
최적의 파라미터를 찾아간다.
그리고 이런 방법을 경사하강법(Gradient Descent)이라 부른다.

### 용어
평균 제곱 오차(mean squared error, MSE)
평균 절대 오차(mean absolute error, MAE)
결정 계수(coefficient of determination)
수렴(converge)
학습률 (Learning Rate)
기울기: coef_
절편: intercept_
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

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
    
    return lr.coef_[0][0], lr

if __name__ == '__main__':
    data = {
        'weight': [65.78,71.52,69.40,68.22,67.79],
        'height': [112.99,136.49,153.03,142.34,144.30],
    }

    df = pd.DataFrame(data)
    
    coef, lr = linear_regression(df.weight.values.reshape(-1,1), df.height.values.reshape(-1,1))
    # 기울기 출력
    print(f'{coef}')

    # 시각화
    plt.plot(df.weight, df.height, 'o')
    plt.plot(df.weight,lr.predict(df.weight.values.reshape(-1,1)))
    plt.show()
