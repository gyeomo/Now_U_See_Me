# Now_U_See_Me

#### 1. 프로젝트 설명  

#### 2. 사용법

#### 3. 개발 환경 및 언어 

#### 4. 시스템 구성 및 아키텍처 

#### 5. 프로젝트 특징

#### 6. 기대효과 및 활용분야  

<br/>

## 1. 프로젝트 설명

[![demo](./descript_image/demo.png)](https://www.youtube.com/watch?v=PKa12XJIs78&feature=youtu.be)
Now_U_See_Me는 CCTV를 이용한 외부인 감지 시스템으로 실시간으로 Rasberry Pi에 설치한 webcam으로부터 얻은 사진을 server로 전송하여 아는 얼굴인지 판별하여 모르는 사람일 경우 Client인 App에 알림을 주는 서비스입니다.  Client가 알림을 통해 받은 사진을 보고 모르는 사람인지 아는 사람인지 결정하여 시스템에 반영할 수 있습니다. 모르는 사람일 경우 112에 신고하세요. 남겨진 사진이 증거가 됩니다.

<br/>

## 2. 사용법

#### 1. 프로젝트를 다운받습니다.

```
` $ git clone https://github.com/gyeomo/Now_U_See_Me.git`
```

#### 2. 링크를 통하여 각 영역 별로 설치를 진행합니다.

- [server](https://github.com/gyeomo/Now_U_See_Me/tree/master/server)
- [Learning](https://github.com/gyeomo/Now_U_See_Me/tree/master/learn) 
- [Client](https://github.com/gyeomo/Now_U_See_Me/tree/master/mobile)
- [Cam](https://github.com/gyeomo/Now_U_See_Me/tree/master/cam) 

#### 3. 기능을 실행합니다.

**Learning 실행**

```bash
1. 터미널 열기
2. cd learn/learning
3. $ python my_utils.py
4. $ python main.py
```

**Server 실행**

```bash
1. 터미널 열기  
2. cd server
3. 'npm start'입력
```

**Client 실행**

[Client](https://github.com/gyeomo/Now_U_See_Me/tree/master/mobile)

**Cam 실행**

```bash
1. cd cam
2. send_file.py의 url 부분에 서버 ip 주소와 Directory 이름 수정
3. $ python send_file.py
```
<br/>

## 3. 개발 환경 및 언어

<img src="/descript_image/language.png">  

- **server**: JavaScript, Express, Node.js, Mysql, Ubuntu 18.0.1  
- **Learning** : Python(Pytorch, OpenCV), Ubuntu 18.0.1  
- **Client** : Android Studio Java, Android 9  
- **Cam** : Linux python

<br/>

## 4. 시스템 구성 및 아키텍처

<img src="/descript_image/System_Structure.png">  

1. 라즈베리파이에 설치한 웹캠을 이용하여 얻은 사진을 server에 Post 요청을 보내 전송한다. 
2. 서버에서 얼굴이 포함된 frame들을 learning process에 넣는다.
3. 아는 사람들(학습된 identities)의 사진은 삭제한다.
   3-1. 모르는 사람들(학습되지 않은 identities)은 한 사람당 하나의 사진을 남기고 지운다.
   3-2. 남겨진 하나의 사진을  Mysql로 만들어진 database에 저장한다.
   3-3. 동시에 client에게 FCM을 이용하여 notification을 보낸다.
4. Client(Android app)에서 notification받은 사진을 보고 아는 사람들의 data에 저장 할지를 결정한다.
5. 결정된 사항을 server로 Post 요청을 보내 전송한다.
6. Learning process의 결과를 바탕으로 사진을 학습해 아는 사람들의 data(family, friends directory)에 반영한다.

<br/>

## 5. 프로젝트 특징

- **실시간 알림** 외부인의 침입에 대한 즉각적인 알림이 간다.  
- **실시간 학습 반영** 클라이언트의 결과에 따라 실시간 학습과 반영을 한다.  
- **적은 데이터 학습** 최소 한 장의 사진으로도 얼굴 식별이 가능하다.  
- **제약이 적은 CCTV 설치** 단순한 웹캠으로 사진을 전송하므로 출입문, 집안 내부 등에 쉽게 설치할 수 있다.  

<br/>
 
## 6. 기대효과 및 활용분야
  
- 사업성  
사람인식 기반의 지능형 CCTV는 보안관제 산업 등과 깊은 연관성을 가지고 있어 IT전반에 대한 기술적/ 경제적 파급효과가 클 것으로 예상된다. 이 기술을 활용하여 미아방지, 범죄자 검색, 국가 시설물 보호뿐만 아니라 일반 가정 등 그 활용이 다양한 분야로 확산되고 이를 통한 간적접인 경제효과가 클 것으로 예상된다.
<br>  
  
- 차별성  
 이 시스템은 대용량의 학습데이터가 필요한 딥러닝 시스템의 단점을 개선하였다. 또한 즉각적인 학습과 예측이 가능한 Real Time  구조로 구성되어 사용자에게 편리함을 제공한다.
