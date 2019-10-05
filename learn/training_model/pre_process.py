import os
import pickle

import cv2 as cv
import mxnet as mx
from mxnet import recordio
from tqdm import tqdm

from config import path_imgidx, path_imgrec, IMG_DIR, pickle_file
from utils import ensure_folder


if __name__ == "__main__":
    ensure_folder(IMG_DIR) 
    imgrec = recordio.MXIndexedRecordIO(path_imgidx, path_imgrec, 'r')
    #임의 액세스를 지원하는 RecordIO 데이터 형식을 읽고 씁니다 .
    
#1~2830147 faces_glintasia file(Asian-celeb dataset)
    samples=[]
    for i in tqdm(range(2830146)):
        try:
            header, s = recordio.unpack(imgrec.read_idx(i+1))
            img = mx.image.imdecode(s).asnumpy()
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            label = int(header.label[:1])
            filename = '{}_{}.png' .format(label,i)
            samples.append({'img': filename, 'label': label})
            filename = os.path.join(IMG_DIR, filename)
            cv.imwrite(filename, img)
        except KeyboardInterrupt:
            raise
        except:
            pass

   
    with open(pickle_file, 'wb') as file:
        pickle.dump(samples, file)
    with open(pickle_file, 'rb') as file:
        data=pickle.load(file)
        print(data)    

    print('num_samples: ' + str(len(samples)))


