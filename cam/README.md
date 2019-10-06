# Now_U_See_Me Cam

## 1. 개발 환경 구축 및 설치
 - Raspberry Pi 3
 - python 2.7
 - opencv 3.4.0


## 2. 사용법  
1. send_file.py가 있는 폴더로 이동
2. url 부분에 서버 ip 주소와 Directory 이름 수정
3. `python send_file.py` 로 실행

## 3. 특징  

### [send_file.py](https://github.com/gyeomo/Now_U_See_Me/blob/master/cam/send_file.py)  

- 0.4초마다 사진을 찍어서 6장을 모으면 서버로 전송한다.  
- 사진 이름은 현재 시간을 시-분-초-밀리초로 변환하여 저장한다.
- 보내진 사진은 삭제한다.

<br>  
<br>   

## Revision history  

[now_u_see_me_cam](https://github.com/kiryun/now_u_see_me_cam)
