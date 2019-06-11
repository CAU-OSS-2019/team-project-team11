import os
import sys

sys.path.append('/Users/moon-il')
sys.path.append('/anaconda3/lib/python3.7/site-packages/IPython/extensions')
sys.path.append('/Users/moon-il/.ipython')
sys.path.remove('/Users/moon-il')
sys.path.remove('/anaconda3/lib/python3.7/site-packages/IPython/extensions')
sys.path.remove('/Users/moon-il/.ipython')

import numpy as np
import tensorflow as tf
import os
import numpy as np
from skimage.io import imread
from skimage.transform import resize



# 현재 test데이터 폴더로 경로를 지정한다.
# test폴더 - drawings, porn, sexy, neutral, hentai메모장을 만들어 놓는다. 해당 메모장에 사진주소로 입력해야 된다.
subset_dir = '/Users/moon-il/Work_Space/PycharmProjects/untitled/nsfw_data_scraper-master/raw_data/test/'
filename_list = os.listdir(subset_dir)  # 현재 그 폴더에 5개의 메모장이 있다.



# 만약 DS_Store 이게 있으면 지우기
for s in filename_list:
    if '.DS_Store' in s:
        filename_list.remove('.DS_Store')
        break;


# 전체 사진 url, 라벨
filename_list_url = []  # 전체 사진url  ######### 수정!!! #########  filename_list2 = []
filename_list_label = []

for i in filename_list:
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
            filename_list_url.append(line)
            filename_list_label.append(i)

        except:
            pass
        if (len(data_t2) == 10):  # 사진 10장씩만 뽑음 -> 총 50장 -> 40장은 train, 10장은 validation
            break





from PIL import Image
import os, glob, numpy as np
from sklearn.model_selection import train_test_split



# 이미지 파일 이름, 파일 라벨

nb_classes = len(filename_list)

image_w = 64
image_h = 64

pixels = image_h * image_w * 3

X = []
y = []

for idx, cat in enumerate(filename_list):

    # one-hot 돌리기.
    label = [0 for i in range(nb_classes)]
    label[idx] = 1


filenames = []
for i, f in enumerate(filename_list_url):
    print(f)
    try:
        img = imread(filename_list_url[i])  # shape: (H, W, 3), range: [0, 255]
        img = resize(img, (image_w, image_h, 3), mode='constant').astype(np.float32)
        data = np.asarray(img)
        filenames.append(f)

        X.append(data)
        y.append(filename_list_label[i])

    except:
        pass

X = np.array(X)



from PIL import Image
import os, glob, numpy as np
from keras.models import load_model


model = load_model('./model/multi_img_classification.model')

prediction = model.predict(X)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
cnt = 0


print(filenames)
for i in prediction:
    pre_ans = i.argmax()  # 예측 레이블
    print(i)
    print(pre_ans)
    pre_ans_str = ''
    if pre_ans == 0: pre_ans_str = "drawings"
    elif pre_ans == 1: pre_ans_str = "hentai"
    elif pre_ans == 2: pre_ans_str = "neutral"
    elif pre_ans == 3: pre_ans_str = "porn"
    else: pre_ans_str = "sexy"
    # 0.8

    if i[0] >= 0.4 : print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[1] >= 0.4: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"으로 추정됩니다.")
    if i[2] >= 0.4: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[3] >= 0.4: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    if i[4] >= 0.4: print("해당 "+filenames[cnt]+"이미지는 "+pre_ans_str+"로 추정됩니다.")
    cnt += 1



# 실행하기 전 해 할 일
#
# 1. 현재 test데이터 폴더로 경로를 지정한다.
#    test폴더 - drawings, porn, sexy, neutral, hentai메모장을 만들어 놓는다. 해당 메모장에 사진주소로 입력해야 된다.
# 2. 14라인에서 데이터 변환 파일 불러오기위해 경로를 수정하고 52라인로 라벨 수를 결정하기위한 파일 리스트 경로를 수정, 101라인에서는 모델 저장경로를 수정
