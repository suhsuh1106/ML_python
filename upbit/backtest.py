import pyupbit
import numpy as np
# OHLCV(open, high, low, close, volume)으로 당일 시가종가 등 데이터 구하기
df = pyupbit.get_ohlcv("KRW-BTC", count=20)

# 변동성 돌파전략 이용 (고가-저가)*0.5
df['range'] = (df['high'] - df['low']) * 0.5

# target(매수가), range col을 한칸씩 밑으로 내림
df['target'] = df['open'] + df['range'].shift(1)

# ror(수익율), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

# 누적 곱 계산 => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")