import os
import shutil
import cv2 as cv
import time
from my_config import *
from my_utils import * 
import client_manager

if __name__ == "__main__":
    cm = client_manager.ClientManager()
    model=model_load()
    th=th_load()
    try:
        while True:
            frlist=[]
            frlist=sorted(os.listdir(frdir))
            #print(frlist)
            if frlist:
                imgdir=move_un(frlist[0].split('.')[0]) #undir+dir_name
                print(imgdir)
                evaluate(model,frlist,th,imgdir)#path is fullpath    
                for frimgs in frlist: #imgs
                    if os.path.isfile(frdir+frimgs):
                        os.remove(frdir+frimgs)
                try: os.rmdir(imgdir)
                except OSError: pass
            time.sleep(1)
            '''
                result={'eventTime':frlist[0],
                       'img_addrs':undata,
                        'types':[1]*len(undata)}
                print(result)
                time.sleep(1)
                
                res = cm.post_status_update(result)
                print(res.status_code)
                if res.status_code==404:
                    if os.path.isdir(undir+frlist[0]):shutil.rmtree(undir+frlist[0])
            famlist=sorted(os.listdir(famdir))
            if famlist:
                add_pickle(model,famdir,famlist)
            frilist=sorted(os.listdir(fridir))
            if frilist:
                add_pickle(model,fridir,frilist)
            '''               
    except KeyboardInterrupt:
        pass   
   