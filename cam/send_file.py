import numpy as np
import cv2
import os
import time
from datetime import datetime
import requests
import urllib2
import urllib

path_dir = './images/'
url = 'http://203.252.91.45:3000/event/upload'

prevTime = 0
cap = cv2.VideoCapture(0) #웹캠 활성화
idx = 0
flag = 0
preTime = time.time()
filename_list = os.listdir(path_dir) #폴더에 있는 파일 목록 불러오기
for each in filename_list:
	os.remove(path_dir+each) #실행초기에 이미지 파일 삭제
while True:
	curTime = time.time()
	ret, frame = cap.read()
	if (curTime - preTime) > 0.4: #0.4초마다 이미지를 저장
		preTime = time.time()
		print 'take'
		
		now = datetime.now()
		current_time = str(now.hour)+"-"+str(now.minute)+"-"+\
				str(now.second)+"-"+str(now.microsecond) #시-분-초-밀리초로 이름을 저장
		cv2.imwrite('./images/'+current_time+'.jpg',frame)
		idx += 1
		if idx >4 : # 이미지가 5장 쌓이면 Flag에 1 인가
			flag =1
			idx = 0
		if flag==1:
			filename_list = os.listdir(path_dir) # 폴더에 있는 목록 불러오기
			file_list = []
			for each in filename_list:
				file_obj = []
				test = path_dir+each
				file_obj.append('file')
				file_obj.append(open(path_dir+each,'rb'))
				file = tuple(file_obj)
				file_list.append(file) # 파일 형식 맞춰주기
				os.remove(path_dir+each) # 파일 삭제
			res = requests.post(url, files=file_list) # 서버로 데이터 전송
			print(res)
			flag = 0
cap.release()
