# Open-Source S/W project - team 11

모자이크(가칭)
====
모자이크는 실시간 스트리밍 환경에서 사람들의 얼굴을 자동으로 모자이크 처리 해줍니다. 

얼굴 모자이크
----
기계학습에 사용한 알고리즘은 신경망 알고리즘들 중에서 Convolutional Neural Network(CNN)을 사용하였습니다. 한국어에서 형태소분석은 자연어처리를 위한 가장 기본적인 전처리 과정이므로 속도가 매우 중요한 요소라고 생각합니다. 따라서 자연어처리에 많이 사용하는 Long-Short Term Memory(LSTM)와 같은 Recurrent Neural Network(RNN) 알고리즘은 속도 면에서 활용도가 떨어질 것으로 예상하여 고려 대상에서 제외하였습니다.

CNN 모델에 대한 상세한 내용은 [CNN 모델](https://github.com/kakao/khaiii/wiki/CNN-%EB%AA%A8%EB%8D%B8) 문서를 참고하시기 바랍니다.

NSFW
----
### 정확도
CNN 모델의 주요 하이퍼 파라미터는 분류하려는 음절의 좌/우 문맥의 크기를 나타내는 win 값과, 음절 임베딩의 차원을 나타내는 emb 값입니다. win 값은 {2, 3, 4, 5, 7, 10}의 값을 가지며, emb 값은 {20, 30, 40, 50, 70, 100, 150, 200, 300, 500}의 값을 가집니다. 따라서 이 두 가지 값의 조합은 6 x 10으로 총 60가지를 실험하였고 아래와 같은 성능을 보였습니다. 성능 지표는 정확률과 재현율의 조화 평균값인 F-Score입니다.

![](.github/img/win_emb_f.png)

win 파라미터의 경우 3 혹은 4에서 가장 좋은 성능을 보이며 그 이상에서는 오히려 성능이 떨어집니다. emb 파라미터의 경우 150까지는 성능도 같이 높아지다가 그 이상에서는 별 차이가 없습니다. 최 상위 5위 중 비교적 작은 모델은 win=3, emb=150으로 F-Score 값은 97.11입니다. 이 모델을 large 모델이라 명명합니다.


### 속도
모델의 크기가 커지면 정확도가 높아지긴 하지만 그만큼 계산량 또한 많아져 속도가 떨어집니다. 그래서 적당한 정확도를 갖는 모델 중에서 크기가 작아 속도가 빠른 모델을 base 모델로 선정하였습니다. F-Score 값이 95 이상이면서 모델의 크기가 작은 모델은 win=3, emb=30이며 F-Score는 95.30입니다.

속도를 비교하기 위해 1만 문장(총 903KB, 문장 평균 91)의 텍스트를 분석해 비교했습니다. base 모델의 경우 약 10.5초, large 모델의 경우 약 78.8초가 걸립니다.


빌드 및 설치
----
khaiii의 빌드 및 설치에 관해서는 [빌드 및 설치 문서](https://github.com/kakao/khaiii/wiki/%EB%B9%8C%EB%93%9C-%EB%B0%8F-%EC%84%A4%EC%B9%98)를 참고하시기 바랍니다.


Contributing
----
khaiii에 기여하실 분들은 [CONTRIBUTING](CONTRIBUTING.md) 및 [개발자를 위한 가이드](https://github.com/kakao/khaiii/wiki#%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%A5%BC-%EC%9C%84%ED%95%9C-%EA%B0%80%EC%9D%B4%EB%93%9C) 문서를 참고하시기 바랍니다.


License
----
This software is licensed under the [Apache 2 license](LICENSE), quoted below.

Copyright 2018 Kakao Corp. <http://www.kakaocorp.com>

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this project except in compliance with the License. You may obtain a copy
of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
