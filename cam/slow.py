import numpy as np
#import imutils
import cv2
import os
import time
from datetime import datetime
import requests
import urllib2
import urllib

path_dir = './images/'
url = 'http://203.252.91.45:3000/event/upload'

print("[INFO] loading face detector...")
protoPath = os.path.sep.join(["face_detection_model", "deploy.prototxt"])
modelPath = os.path.sep.join(["face_detection_model",
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
prevTime = 0
cap = cv2.VideoCapture(0)
idx = 0
flag = 0
preTime = time.time()
while True:
	curTime = time.time()
	ret, frame = cap.read()
	'''
	frame= cv2.resize(frame, dsize=(500,500),interpolation=cv2.INTER_AREA)
	(h, w) = frame.shape[:2]
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()

	if len(detections) > 0:
		i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]

		if confidence > 0.7:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			if ((endX-startX)<120) or ((endY-startY)<120):
				continue
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
			#if fW < 15 or fH < 15:
			#	continue

			#cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 1)
			idx+=1
			if idx>1:
				flag = 1
				idx=0
			prevTime = time.time()
			sec = prevTime - curTime
			fps = 1/(sec)
			str_fps = "FPS : %0.1f" % fps
			print str_fps
	'''
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
		


#        cv2.putText(frame, str_fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
#	cv2.imshow("Image", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
		
cap.release()
#cv2.destroyAllWindows()
