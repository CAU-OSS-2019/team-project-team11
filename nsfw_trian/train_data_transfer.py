import os
import sys
import numpy as np
import tensorflow as tf
import os
import numpy as np
from skimage.io import imread
from skimage.transform import resize

sys.path.append('/Users/moon-il')
sys.path.append('/anaconda3/lib/python3.7/site-packages/IPython/extensions')
sys.path.append('/Users/moon-il/.ipython')
sys.path.remove('/Users/moon-il')
sys.path.remove('/anaconda3/lib/python3.7/site-packages/IPython/extensions')
sys.path.remove('/Users/moon-il/.ipython')


# 현재 traine데이터 폴더로 경로를 지정한다.
# train폴더 - drawings, porn, sexy, neutral, hentai메모장을 만들어 놓는다. 해당 메모장에 사진주소로 입력해야 된다.
subset_dir = '/Users/moon-il/Work_Space/PycharmProjects/untitled/nsfw_data_scraper-master/raw_data/train/'
filename_list = os.listdir(subset_dir)
# 현재 그 폴더에 5개의 메모장이 있다.


# 위에서 filename_list에서 DS_Store란 파일이 생겨 직접 지우기
for s in filename_list:
    if '.DS_Store' in s:
        filename_list.remove('.DS_Store')
        break;


# 전체 사진 url, 라벨
filename_list_url = []
filename_list_label = []

# 데이터 출력
for i in filename_list:
    print(i)
    f = open(subset_dir + i, 'r')
    lines = f.readlines()

    # 각 url에서 \n없애기
    data_t = []
    for ii in lines:
        data_t.append(ii[:-1])

    data_t2 = []
    for line in data_t:
        try:
            data_t2.append(line)
            print(line)

            filename_list_url.append(line)
            filename_list_label.append(i)
        except:
            pass
        if (len(data_t2) == 10000):  # 각 라벨당 몇장씩 뽑을지 결정하기 -> 10을 입력한다면 -> 사진 10장씩만 뽑음 -> 총 50장 -> 40장은 train, 10장은 validation
            break



# 데이터 변환


from PIL import Image
import os, glob, numpy as np
from sklearn.model_selection import train_test_split



# 파일 리스트 길이 출력
nb_classes = len(filename_list)

# 우린 64*64로 사진shape변환
image_w = 64
image_h = 64

pixels = image_h * image_w * 3

X = []
y = []


# 라벨 데이터 생성
for idx, cat in enumerate(filename_list):

    # one-hot 돌리기.
    label = [0 for i in range(nb_classes)]
    print(label)
    label[idx] = 1
    print(label)


for i, f in enumerate(filename_list_url):
    print(filename_list_label[i])
    print(f)
    if i % 100 == 0:
        print(i)
    try:
        img = imread(filename_list_url[i])  # shape: (H, W, 3), range: [0, 255]
        img = resize(img, (image_w, image_h, 3), mode='constant').astype(np.float32)
        data = np.asarray(img)

        X.append(data)
        y.append(filename_list_label[i])

    except:
        pass

X = np.array(X)
y = np.array(y)
print(X)
print(y)
# 1 0 0 0 0이면 drawings
# 0 1 0 0 0이면 hentai


X_train, X_test, y_train, y_test = train_test_split(X, y)
xy = (X_train, X_test, y_train, y_test)
np.save("./numpy_data/multi_image_data.npy", xy)
# 직접 경로 수정하기

print("ok", len(y))


# 실행하기 전 해야 할 일
# 1. 현재 traine데이터 폴더로 경로를 지정한다.
#    train폴더 - drawings, porn, sexy, neutral, hentai메모장을 만들어 놓는다. 해당 메모장에 사진주소로 입력해야 된다.
# 2.  20라인, 117라인에서 데이터 불러오기(subset_dir), 데이터 변환 저장하기(np.save) 경로를 해당 로컬에 맞게 수정해줘야 한다.

