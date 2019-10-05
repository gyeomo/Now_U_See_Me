
import sys
import numpy as np
import cv2
import time
import os
from datetime import datetime
import requests
import urllib2
import urllib
#import csv
#import logging
#import datetime
path_dir = './images/'
url = 'http://203.252.91.45:3000/event/upload'
# #test
# res = requests.get('http://127.0.0.1:3000/users')
# print(res)



#all_count = 0     #Checking finding count
#true_count = 0    #Checking detection count

#def mylog(start_time, end_time, count):   #show real-time result
#    print ('st:%s, et:%s, cnt:%s', start_time, end_time, count)

#open result CSV file
#file = open('./result/res_Insert_name.csv', 'w')

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
i=0
flag = 0

#one_m_timer_start = time.time()
while 1:
   
    s = time.clock()  #Start time
    ret, img = cap.read()
    img = cv2.resize(img, dsize=(500,500), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,\
		scaleFactor=1.1,\
		minSize=(100,100))
 #   all_count = all_count + 1  #Plus finding count
    for (x, y, w, h) in faces:
        face = face_cascade.detectMultiScale(gray,\
		scaleFactor=1.1,\
		minSize=(150,150))
        for (x_, y_, w_, h_) in face:
            cv2.rectangle(img,(x_,y_),(x_+w_,y_+h_),(255,0,0),2)
            now = datetime.now()
            current_time = str(now.year)+"-"+\
                          str(now.month)+"-"+str(now.day)+"-"+\
                          str(now.hour)+"-"+str(now.minute)+"-"+\
                          str(now.second)+"-"+str(now.microsecond)
            cv2.imwrite('./images/'+current_time+'.jpg',img)
            i+=1
            if i >5:
                flag = 1
                print('send!!!!!') 
  #      roi_gray = gray[y:y+h, x:x+w]
  #      roi_color = img[y:y+h, x:x+w]
  #      true_count = true_count + 1
    e = time.clock()  #Finish time
    print(str(1/(e-s)))
    if flag==1:
        test = 0
        filename_list = os.listdir(path_dir)
        #filename_list.remove(".DS_Store")
        file_list = []
        for each in filename_list:
            file_obj = []
            test = path_dir+each
            file_obj.append('file')
            file_obj.append(open(path_dir+each,'rb'))
            file = tuple(file_obj)
            file_list.append(file)
            os.remove(path_dir+each)
        #test = open(test, 'rb')
        #post_data = {'file': test, 'output':'json'}
        #request = urllib2.Request(url, data = urllib.urlencode(post_data))
        #response = urllib2.urlopen(request)
        res = requests.post(url, files=file_list)
        print res
        flag = 0
        break
  #      msg = str(s) + ',' + str(e) + ',' + str(e-s) + ',' + str(true_count) +'\n'
  #      file.write(msg)  #writing about start time, end time, spend time, face detection count

  #      mylog('','',msg)

  #  one_m_timer_end = time.time()
  #  if( one_m_timer_end - one_m_timer_start > 10 ):   #10seconds program run
  #      print one_m_timer_end - one_m_timer_start
  #      break

  #  cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff  #If you press "ESC" button on your keyboard program is end
    if k == 27:
        break

cap.release()

#cv2.destroyAllWindows()
#file.close()

#print "All count :" , all_count    #show all_count
#print "Detection count :" , true_count    #show detection count
