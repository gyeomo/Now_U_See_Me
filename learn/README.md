# Now_U_See_Me Learning process

#### 1. 소개

#### 2. 특징

#### 3. 사용법

#### 4. 실행 결과

#### 5. 라이선스



## 1. 프로젝트 소개

Learning process는 두 가지 일을 처리합니다.

-server에서 받아오는 웹캠 frame에서 얼굴 영역을 crop 하고 기존의 Data들과 비교합니다.

비교한 결과가 외부인일 경우, client에게 통지를 줄 수 있도록 처리합니다.

-client에게 얻은 외부인 결과를 통해 기존의 Data(family or friends)들에 포함 할 수 있도록 처리합니다.

## 2. 특징

<video src="./readme_image/real_time_face_cam.mp4"></video>

**사용된 모델 성능 demo 영상입니다.**



## 3. 사용법

2-1. 해당 프로젝트를 다운받고 training_model 디렉토리로 이동합니다.

```bash
 $ git clone https://github.com/gyeomo/Now_U_See_Me.git
```

2-2. **개발환경 구축** [training_model](https://github.com/gyeomo/Now_U_See_Me/tree/master/learn/training_model) 디렉토리의 README.md 를 보고 따라합니다.

2-3. **파일 복사**  2-2에서 생성된 파일을 `learn/learning/`디렉토리에 복사합니다.

```bash
learn/training_model/InsightFace-v2/BEST_checkpoint.tar
learn/training_model/InsightFace-v2/data/thereshold.txt
```

2-4. **디렉토리 생성** 시스템에 필요한 디렉토리들을 생성합니다.

![dire](/home/lmrider/Desktop/readme_image/dire.png)

```
fr
```



## 5. 라이선스![apm](https://img.shields.io/apm/l/vim-mode.svg)

The code of InsightFace is released under the MIT License. There is no limitation for both acadmic and commercial usage.

The training data containing the annotation (and the models trained with these data) are available for non-commercial research purposes only.

















