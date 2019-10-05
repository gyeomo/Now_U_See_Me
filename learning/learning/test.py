'''a=['a','a','b','a','b','c','b','e','d']
data=[]
dst=[]
for i in a:
    data.append({'identity':'unknown','img':i})
print(data)

for i,data1 in enumerate(data):
    if data1['identity']=='unknown':
        data1['identity']=i
        data2['identity']=[i for j,data2 in enumerate(data,i+1) if data1['img']==data2['img']]
for i,img in enumerate(data):
    if img['identity']==i: dst.append(img)
print(dst)

'''
import os
import shutil
import datetime

file=datetime.datetime.today()
a='{0}-{1}-{2}-{3}-{4}-{5}-{6}.jpg'.format(file.year,file.month,file.day,file.hour,file.minute,file.second,file.microsecond)

print('../now_u_see_me_server/fresh/{}'.format(a))


'''
def add_pickle(model,imgdir,imgslist,th):
    where=imgdir.split('/')[1]
    kndatas=kndata_load()
    for imglist in imgslist:
        imgpath=imgdir+imglist
        is_valid, bounding_boxes, landmarks = get_central_face_attributes(imgpath)
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