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
cap = cv2.VideoCapture(0)
idx = 0
flag = 0
preTime = time.time()
filename_list = os.listdir(path_dir)
for each in filename_list:
	os.remove(path_dir+each)
while True:
	curTime = time.time()
	ret, frame = cap.read()
	if (curTime - preTime) > 0.4:
		preTime = time.time()
		print 'take'
		
		now = datetime.now()
		current_time = str(now.year)+"-"+\
				str(now.month)+"-"+str(now.day)+"-"+\
				str(now.hour)+"-"+str(now.minute)+"-"+\
				str(now.second)+"-"+str(now.microsecond)
		cv2.imwrite('./images/'+current_time+'.jpg',frame)
		idx += 1
		if idx >5 :
			flag =1
			idx = 0
		if flag==1:
			filename_list = os.listdir(path_dir)
			file_list = []
			for each in filename_list:
				file_obj = []
				test = path_dir+each
				file_obj.append('file')
				file_obj.append(open(path_dir+each,'rb'))
				file = tuple(file_obj)
				file_list.append(file)
				os.remove(path_dir+each)
			res = requests.post(url, files=file_list)
			print(res)
			flag = 0
cap.release()
