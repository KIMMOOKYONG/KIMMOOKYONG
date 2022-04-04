import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema

# Generate a noisy AR(1) sample
findType = 'slow'   # 빠른/느린 최고/최저값 구하기 선택
np.random.seed(0)
rs = np.random.randn(200)
xs = [0]
for r in rs:
    xs.append(xs[-1] * 0.9 + r)
df = pd.DataFrame(xs, columns=['data'])

n = 5  # number of points to be checked before and after

# Find local peaks
if findType == 'slow':
    df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
    df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal, order=n)[0]]['data']
else:
    df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
    df['max'] = df.data[(df.data.shift(1) < df.data) & (df.data.shift(-1) < df.data)]

# Plot results
plt.scatter(df.index, df['min'], c='r')
plt.scatter(df.index, df['max'], c='g')
plt.plot(df.index, df['data'])
plt.show()
