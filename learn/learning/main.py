import os
import shutil
import cv2 as cv
import time
from my_config import *
from my_utils import * 
import client_manager

if __name__ == "__main__":
    #server calls & learning model load 
    cm = client_manager.ClientManager()
    model=model_load()
    th=th_load()

    try:
        while True:
            kndatas=kndatas_load()# known data load

            #unknown images detector
            frlist=sorted(os.listdir(frdir))
            if frlist:

                #move the unpro dir
                eventdir=frlist[0].split('.')[0]
                middir=make_dir(uprdir,eventdir) #path is [uprdir/eventdir]
                undata=compare(model,th,frlist,frdir,middir,kndatas,1) #compare the new images with the known data 
                #undata=evaluate(model,frlist,th,imgdir)#path is the fullpath
                remove_file(frdir,frlist) #delete the fresh imgs
                try: #if empty the middir
                    os.rmdir(middir)
                    continue
                except OSError: pass

                #move unknown dir
                dstdir=make_dir(undir,eventdir)#path is [undir/eventdir]
                un_compare(model,undata,th,dstdir)
                print(dstdir)
                if os.path.isdir(middir):shutil.rmtree(middir)

                #send the unknown images to the server    
                unknown=sorted(os.listdir(dstdir))
                result={'eventTime':dstdir.split('/')[-1],
                       'img_addrs':unknown,
                        'types':['unknown']*len(unknown)} 
                res = cm.post_status_update(result)
                print(res.status_code)
                if res.status_code==404:
                    if os.path.isdir(dstdir):shutil.rmtree(dstdir)
                time.sleep(0.5)

            #Iearn the unknown image == Create the new identities    
            famlist=sorted(os.listdir(famdir))
            frilist=sorted(os.listdir(fridir))
            if famlist:
                dume=compare(model,th,famlist,famdir,kndir,kndatas,0)
                #add_pickle(model,famdir,famlist,th)
                time.sleep(0.5)
            elif frilist:
                dume=compare(model,th,frilist,fridir,kndir,kndatas,0)
                #add_pickle(model,fridir,frilist,th)
                time.sleep(0.5)
            time.sleep(1) 
                            
    except KeyboardInterrupt:
        pass
