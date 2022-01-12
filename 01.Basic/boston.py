# 입력으로 0에서 100 사이의 정수값을 받아서
# 보스턴 주택가격의 실제값과 예측값을 보여주는 프로그램
# import part
import numpy as np
import pandas as pd
import tensorflow as tf
import warnings
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 상수값 설정 등 변수 초기화
seed = 2022
warnings.filterwarnings('ignore')
np.random.seed(seed)
tf.random.set_seed(seed)
boston = load_boston()
X_train, X_test, y_train, y_test = train_test_split(
    boston.data, boston.target, test_size=0.1, random_state=seed
)

# 메인 모델 만들기
model = Sequential([
                    Dense(30, input_dim = 13, activation = 'relu'),
                    Dense(12, activation = 'relu'),
                    Dense(1)                        # 회귀의 경우 activation 함수를 지정하지 않는다
])
model.compile(optimizer='adam', loss = 'mean_squared_error')
model.fit(X_train, y_train, epochs=500, batch_size=60, 
          validation_split=0.1, verbose=0)

# 입력값 받기
index = int(input('0 ~ 100 정수값을 입력하세요.> '))
test = X_test[index].reshape(1, -1)
pred_value = model.predict(test)

# 최종결과 출력
print(f'실제값 : {y_test[index]}, 예측값 : {pred_value[0,0]: .2f}')