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
            frlist=sorted(os.listdir(frdir))
            if frlist:
                dirname=frlist[0].split('.')[0]
                imgdir=move_dir(uprdir,dirname) #undir+dir_name
                undata=evaluate(model,frlist,th,imgdir)#path is fullpath
                for frimgs in frlist: #imgs
                    if os.path.isfile(frdir+frimgs):
                        os.remove(frdir+frimgs)
                try: 
                    os.rmdir(imgdir)
                    continue
                except OSError: pass
                dst=move_dir(undir,dirname)
                un_compare(model,undata,th,dst)
                print(dst)
                if os.path.isdir(imgdir):
                    shutil.rmtree(imgdir)
                un=sorted(os.listdir(dst))
                result={'eventTime':dst.split('/')[-1],
                       'img_addrs':un,
                        'types':['unknown']*len(un)} 
                res = cm.post_status_update(result)
                print(res.status_code)
                if res.status_code==404:
                    if os.path.isdir(undir+frlist[0]):shutil.rmtree(undir+frlist[0])
                time.sleep(0.5)
            famlist=sorted(os.listdir(famdir))
            frilist=sorted(os.listdir(fridir))
            if famlist:
                add_pickle(model,famdir,famlist,th)
                time.sleep(0.5)
            elif frilist:
                add_pickle(model,fridir,frilist,th)
                time.sleep(0.5)
            time.sleep(1) 
                            
    except KeyboardInterrupt:
        pass