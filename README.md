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

opencv 라이브러리의 cv2.CascadeClassifier을 이용한 Face detection,
new face일 경우 recognition을 한 뒤 known/unknown으로 분류하여 모자이크 여부를 결정한다.
이후 dlib.correlation_trakcer()를 이용한 face tracking.

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
