import os, glob, numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import keras.backend.tensorflow_backend as K
import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

# 변환한 데이터 불러오기
X_train, X_test, y_train, y_test = np.load('./numpy_data/multi_image_data.npy')
print(X_train.shape)
print(X_train.shape[0])



y_temp1 = y_train
y_train = []
for label in y_temp1:
    if label == 'drawings.txt':
        y_train.append(0)
    elif label == 'hentai.txt':
        y_train.append(1)
    elif label == 'neutral.txt':
        y_train.append(2)
    elif label == 'porn.txt':
        y_train.append(3)
    else:  # label == 'sexy'
        y_train.append(4)

y_temp2 = y_test
y_test = []
for label in y_temp2:
    if label == 'drawings.txt':
        y_test.append(0)
    elif label == 'hentai.txt':
        y_test.append(1)
    elif label == 'neutral.txt':
        y_test.append(2)
    elif label == 'porn.txt':
        y_test.append(3)
    else:  # label == 'sexy'
        y_test.append(4)

print(y_test)


#  nb_classes를 출력하기 위해
subset_dir = '/Users/moon-il/Work_Space/PycharmProjects/untitled/nsfw_data_scraper-master/raw_data/train/'
filename_list = os.listdir(subset_dir)  # 현재 그 폴더에 5개의 메모장이 있다.

# 만약 DS_Store 이게 있으면 지우기
for s in filename_list:
    if '.DS_Store' in s:
        filename_list.remove('.DS_Store')
        break;

nb_classes = len(filename_list)


#일반화
X_train = X_train.astype(float) / 255
X_test = X_test.astype(float) / 255


with K.tf_ops.device('/device:GPU:0'):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=X_train.shape[1:], activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model_dir = './model'

    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    model_path = model_dir + '/multi_img_classification.model'
    print(model_path)
    checkpoint = ModelCheckpoint(filepath=model_path, monitor='val_loss', verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=6)

print(checkpoint)
print(early_stopping)


model.summary()

from keras.models import load_model
model.save('./model/multi_img_classification.model')
# 어디에 모델 저장할지

# batch_size=32, epochs=50
history = model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test), callbacks=[checkpoint, early_stopping])

print("정확도 : %.4f" % (model.evaluate(X_test, y_test)[1]))



y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = np.arange(len(y_loss))

plt.plot(x_len, y_vloss, marker='.', c='red', label='val_set_loss')
plt.plot(x_len, y_loss, marker='.', c='blue', label='train_set_oss')
plt.legend()
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid()
plt.show()





# 실행하기 전 해야 할 일
# 1. 14라인에서 데이터 변환 파일 불러오기위해 경로를 수정하고 52라인로 라벨 수를 결정하기위한 파일 리스트 경로를 수정, 101라인에서는 모델 저장경로를 수정

