import os
import torch
import pickle
import cv2 as cv
import numpy as np
import scipy.stats
import math
import shutil
import time
from PIL import Image
from my_config import *
from utils import align_face,get_all_face_attributes,get_central_face_attributes,draw_bboxes
"""""""""""""""""""""""""""""""""""""""""""""""
utils
"""""""""""""""""""""""""""""""""""""""""""""""
#load learning model
def model_load():
    checkpoint = 'BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model']
    model = model.to(device)
    model.eval()
    return model
#load the comare thereshold value
def th_load():
    with open('thereshold.txt', 'r') as file:
        th=float(file.readline())
    return th
#load the known data
def kndatas_load():
    with open(knpkl, 'rb') as f:
        datas = pickle.load(f)   #'data'={'full_path','identity','img'}   
    return datas

def make_dir(dstdir,dirname):
    if not os.path.isdir(dstdir+dirname):
        os.mkdir('{0}{1}'.format(dstdir,dirname))
    return dstdir+dirname
    
def remove_file(srcdir,imgslist):
    for img in imgslist:
            path=srcdir+img
            if os.path.isfile(path): os.remove(path)

#change the image to one that is suitable for learning.
def get_image(full_path,landmarks, transformer):
    img = align_face(full_path, landmarks)  # BGR
    img = img[..., ::-1]  # RGB
    img = Image.fromarray(img, 'RGB')  # RGB
    img = transformer(img)
    img = img.to(device)
    return img

"""""""""""""""""""""""""""""""""""""""""""""""
service function
"""""""""""""""""""""""""""""""""""""""""""""""
def compare(model,th,newimgs,srcdir,dstdir,kndatas,crop):
    data=[]
    where=srcdir.split('/')[1]
    for newimg in newimgs: #.jpg imgs
        newpath=srcdir+newimg #img fullpath
        is_valid, bounding_boxes, landmarks =get_all_face_attributes(newpath)#face detector
        if is_valid: #If a face exists in a new image, compare it to the existing data
            with torch.no_grad():
                for i,box in enumerate(bounding_boxes): #bounding_boxes is the coordinates of faces
                    if crop:# alignment face
                        new=get_image(newpath,landmarks[i],transformer) 
                    else:
                        new=get_image(newpath,landmarks[0],transformer)
                    imgs = torch.zeros([2, 3, 112, 112], dtype=torch.float)
                    imgs=imgs.to(device) #gpu
                    imgs[0]=new
                    for kndata in kndatas:
                        knimg=kndata['img']
                        imgs[1]=knimg
                        output = model(imgs)
                        feature0 = output[0].cpu().numpy()
                        feature1 = output[1].cpu().numpy()
                        x0 = feature0 / np.linalg.norm(feature0)
                        x1 = feature1 / np.linalg.norm(feature1)
                        cosine = np.dot(x0, x1)
                        try:theta = math.acos(cosine)
                        except  ValueError: theta=20
                        theta = theta * 180 / math.pi
                        if theta<th:
                            if crop: 
                                print('known')
                            break
                        if kndata==kndatas[-1]: #if unknown
                            img=Image.open(newpath)
                            if crop: # new images send to unknown dir
                                img_trim=img.crop((box[0]-35,box[1]-35,box[2]+70,box[3]+70))
                                img_trim.save('{0}/{1}-{2}'.format(dstdir,i,newimg))
                                data.append({'fullpath':'{0}/{1}-{2}'.format(dstdir,i,newimg),'identity':'unknown','img':imgs[0]})
                            else: # learn the images(family or friends)
                                img.save(dstdir+where+'/'+newimg)
                                kndatas.append({'fullpath':dstdir+where+'/'+newimg,'identity':where,'img':imgs[0]})
    if not crop:#The learned image is reflected in the existing data.
        with open(knpkl,'wb') as f:
            pickle.dump(kndatas, f ,pickle.HIGHEST_PROTOCOL)
        remove_file(srcdir,newimgs)
    return data
                           
                            
#The same person's image as one of the unknown images leaves only one image behind.
def un_compare(model,data,th,dst):
    for i,data1 in enumerate(data):
        with torch.no_grad():
            imgs = torch.zeros([2, 3, 112, 112], dtype=torch.float)
            imgs=imgs.to(device)
            if data1['identity']=='unknown':
                data1['identity']=i
                imgs[0]=data1['img']
                for j,data2 in enumerate(data,i+1):
                    imgs[1]=data2['img']
                    output = model(imgs)
                    feature0 = output[0].cpu().numpy()
                    feature1 = output[1].cpu().numpy()
                    x0 = feature0 / np.linalg.norm(feature0)
                    x1 = feature1 / np.linalg.norm(feature1)
                    cosine = np.dot(x0, x1)
                    try:theta = math.acos(cosine)
                    except  ValueError: theta=20
                    theta = theta * 180 / math.pi
                    if theta<th:
                        data2['identity']=i
    for i,img in enumerate(data):
        if img['identity']==i: 
            shutil.copy(img['fullpath'],dst)


#An initialization function that people images in the known dir as pickle files.
def make_pickle():
    data=[]
    model_load()
    classes = [ide for ide in os.listdir(kndir) if os.path.isdir(os.path.join(kndir, ide))] #[family,friends]
    for ide in classes:
        files=[kndir+ide+'/'+img for img in os.listdir(kndir+ide)]#[fullpaths]
        for file in files:
            is_valid, bounding_boxes, landmarks = get_central_face_attributes(file)
            if is_valid:
                img=get_image(file,landmarks,transformer)
                data.append({'fullpath':file,'identity':ide,'img':img})
    with open(knpkl,'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    make_pickle()
    print(kndatas_load())

