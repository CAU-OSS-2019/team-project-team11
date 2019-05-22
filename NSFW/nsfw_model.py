import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
import tensorflow as tf
import keras

import os
currentPath = os.getcwd()  # 작업공간 설정
os.chdir("/Users/moon-il/Downloads/")

from keras.models import load_model   #.h5 모델을 활용하기 위해

model = load_model('nsfw_mobilenet2.224x224.h5')

model.summary() # 입력픽셀값은 224*224*3


# 이미지 테스트 해보기
import matplotlib.pyplot as plt
#%matplotlib inline

test_num = plt.imread('/Users/moon-il/Desktop/batch_모델1.jpg')
test_num = test_num.reshape((1, 224, 224, 3))  # 입력 픽셀행렬이 이렇게 되야 한다!!!

print('The Answer is ', model.predict(test_num))  # 이 model에는 predict_classes가 없다
# The Answer is  [[0.26165554 0.01138252 0.7228562  0.0031485  0.0009572 ]]
# 카테고리 = [ ' 그림 ' , ' 헨타이 ' , ' 중립적 인 ' , ' 포르노 ' , ' 섹시한 ' ]

# 고민 : [섹시한]에 가까울 것 같은데 중립으로 나와있다.



