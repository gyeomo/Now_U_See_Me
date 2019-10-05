import os
import torch
import pickle
import cv2 as cv
import numpy as np
import scipy.stats
import math
import shutil
from PIL import Image
from my_config import *
from utils import align_face,get_all_face_attributes,get_central_face_attributes,draw_bboxes
def model_load():
    checkpoint = 'BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model']
    model = model.to(device)
    model.eval()
    return model

def th_load():
    with open('thereshold.txt', 'r') as file:
        th=float(file.readline())
    return th
def kndata_load():
    with open(knpkl, 'rb') as f:
        datas = pickle.load(f)   #'data'={'full_path','identity','img'}   
    return datas

def move_un(dirname):
    print(dirname)
    #make img_dir
    if not os.path.isdir(undir+dirname):
        os.mkdir('{0}{1}'.format(undir,dirname))
    return undir+dirname

def get_image(full_path,landmarks, transformer):
    img = align_face(full_path, landmarks)  # BGR
    img = img[..., ::-1]  # RGB
    img = Image.fromarray(img, 'RGB')  # RGB
    img = transformer(img)
    img = img.to(device)
    return img

def evaluate(model,frlist,th,imgdir):
    kndatas=kndata_load()
    for frimgs in frlist: #imgs
        frdata=frdir+frimgs
        is_valid, bounding_boxes, landmarks =get_all_face_attributes(frdata)
        if is_valid:
            with torch.no_grad():
                for i,box in enumerate(bounding_boxes):      #1 img
                    frimg=get_image(frdata,landmarks[i],transformer)
                    imgs = torch.zeros([2, 3, 112, 112], dtype=torch.float)
                    imgs=imgs.to(device)
                    imgs[0]=frimg
                    for kndata in kndatas:
                        knimg=kndata['img']
                        imgs[1]=knimg
                        output = model(imgs)
                        feature0 = output[0].cpu().numpy()
                        feature1 = output[1].cpu().numpy()
                        x0 = feature0 / np.linalg.norm(feature0)
                        x1 = feature1 / np.linalg.norm(feature1)
                        cosine = np.dot(x0, x1)
                        theta = math.acos(cosine)
                        theta = theta * 180 / math.pi
                        if theta<th: break
                        if kndata==kndatas[-1]:
                            img=Image.open(frdata)
                            img_trim=img.crop((box[0],box[1],box[2],box[3]))
                            img_trim.save('{0}/{1}-{2}'.format(imgdir,i,frimgs))
 
def add_pickle(model,imgdir,imgslist,th):
    where=imgdir.split('/')[1]
    kndatas=kndata_load()
    for imglist in imgslist:
        imgpath=imgdir+imglist
        is_valid, bounding_boxes, landmarks = get_central_face_attributes(imgpath)
        print(is_valid)
        if is_valid:
            with torch.no_grad():
                data=get_image(imgpath,landmarks,transformer)
                imgs = torch.zeros([2, 3, 112, 112], dtype=torch.float)
                imgs=imgs.to(device)
                imgs[0]=data
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
                    if theta<th: break
                    else :
                        image=Image.open(imgpath)
                        image.save(kndir+where+'/'+imglist)
                        kndatas.append({'fullpath':imgpath,'identity':where,'img':imgs[0]}) 
    with open(knpkl,'wb') as f:
        pickle.dump(kndatas, f ,pickle.HIGHEST_PROTOCOL)
    for imglist in imgslist:
        imgpath=imgdir+imglist
        if os.path.isfile(imgpath):
            os.remove(imgpath)    
'''
def add_pickle(model,imgdir,imgs):
    where=imgdir.split('/')[1]
    datas=kndata_load()
    for img in imgs:
        imgpath=os.path.join(imgdir,img)
        is_valid, bounding_boxes, landmarks = get_central_face_attributes(imgpath)
        print(is_valid)
        data=get_image(imgpath,landmarks,transformer)
        image=Image.open(imgpath)
        image.save(kndir+where+'/'+img)
        datas.append({'fullpath':imgpath,'identity':where,'img':data}) 
    with open(knpkl,'wb') as f:
        pickle.dump(datas, f ,pickle.HIGHEST_PROTOCOL)
    for img in imgs:
        imgpath=os.path.join(imgdir,img)
        if os.path.isfile(imgpath):
            os.remove(imgpath)
 '''   
def make_pickle():
    data=[]
    model_load()
    classes = [ide for ide in os.listdir(kndir) if os.path.isdir(os.path.join(kndir, ide))] #[family,friends]
    for ide in classes:
        files=[kndir+ide+'/'+img for img in os.listdir(kndir+ide)]#[fullpaths]
        for file in files:
            is_valid, bounding_boxes, landmarks = get_central_face_attributes(file)
            img=get_image(file,landmarks,transformer)
            data.append({'fullpath':file,'identity':ide,'img':img})
    with open(knpkl,'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    make_pickle()
    print(kndata_load())

