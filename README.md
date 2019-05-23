# Open-Source S/W project - team 11

Besaic
====
Besaic는 실시간 스트리밍 환경에서 사람들의 얼굴을 자동으로 모자이크 처리 해줍니다. 또한 방송에 부적합한 음란한 내용을 NSFW(Not suitable for work)셋을 이용해 모자이크 합니다.

Reference
----
Face recognition : https://github.com/ageitgey/face_recognition
Face tracking : https://github.com/gdiepen/face-recognition
NSFW training data :  https://github.com/alexkimxyz/nsfw_data_scraper
NSFW pre-trained model :  https://github.com/GantMan/nsfw_model

얼굴 모자이크
----

기계학습에 사용한 알고리즘은 신경망 알고리즘들 중에서 Convolutional Neural Network(CNN)을 사용하였습니다. 한국어에서 형태소분석은 자연어처리를 위한 가장 기본적인 전처리 과정이므로 속도가 매우 중요한 요소라고 생각합니다. 따라서 자연어처리에 많이 사용하는 Long-Short Term Memory(LSTM)와 같은 Recurrent Neural Network(RNN) 알고리즘은 속도 면에서 활용도가 떨어질 것으로 예상하여 고려 대상에서 제외하였습니다.

CNN 모델에 대한 상세한 내용은 [CNN 모델](https://github.com/kakao/khaiii/wiki/CNN-%EB%AA%A8%EB%8D%B8) 문서를 참고하시기 바랍니다.

NSFW
----
# NSFW Detection Machine Learning Model
Trained on 60+ Gigs of data to identify:
- `drawings` - safe for work drawings (including anime)
- `hentai` - hentai and pornographic drawings
- `neutral` - safe for work neutral images
- `porn` - pornographic images, sexual acts
- `sexy` - sexually explicit images, not pornography

This model powers [NSFW JS](https://github.com/infinitered/nsfwjs) - [More Info](https://shift.infinite.red/avoid-nightmares-nsfw-js-ab7b176978b1)

빌드 및 설치
----
```console
pip install cmake dlib opencv-python face_recognition numpy
```

#  Minimum UI

1. 빌드를 위해 필요한 것들
* PyQT5
* Python 3. over
2. Code preview
```python
layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)
        self.btn = QPushButton("NSFW")
        layout.addWidget(self.btn)
        self.le = QLabel("")

        layout.addWidget(self.le)
        self.btn.clicked.connect(self.getfile)
        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)
```
* start button 은 모자이크 처리를 시작을 뜻함
* NSFW button 은 이미지를 받아와서 NSFW 필터링을

## Usage
<<<<<<< HEAD
```python face_recog&mosaic.py
=======
```python
from nsfw_detector import NSFWDetector
detector = NSFWDetector('./nsfw.299x299.h5')
>>>>>>> master
```

## Demo
- https://www.youtube.com/watch?v=_IUhD4zoYuI
