import math
import os
import pickle
import tarfile
import time

import cv2 as cv
import numpy as np
import scipy.stats
import torch
from PIL import Image
from matplotlib import pyplot as plt
from tqdm import tqdm

from config import device
from data_gen import data_transforms
from utils import align_face, get_central_face_attributes, get_all_face_attributes, draw_bboxes
"""

Test learning model using LFW DATASET 

"""

angles_file = 'data/angles.txt'
lfw_pickle = 'data/lfw_funneled.pkl'

def extract(filename):
    with tarfile.open(filename, 'r') as tar:
        tar.extractall('data')

#Make pickle using lfw dataset 
def process():
    #전체 img폴더 불러오기 
    subjects = [d for d in os.listdir('data/lfw_funneled') if os.path.isdir(os.path.join('data/lfw_funneled', d))]
    #개수 안맞으면 오류
    assert (len(subjects) == 5749), "Number of subjects is: {}!".format(len(subjects))

    file_names = []
    for i in range(len(subjects)):
        sub = subjects[i] #각 이미지 폴더 넣기 
        folder = os.path.join('data/lfw_funneled', sub)
        #각 폴더별 jpg 파일 files에 넣기 
        files = [f for f in os.listdir(folder) if
                 os.path.isfile(os.path.join(folder, f)) and f.lower().endswith('.jpg')]
        #jpg 마다 파일경로 레이블 폴더이름 넣기
        for file in files:
            filename = os.path.join(folder, file)
            file_names.append({'filename': filename, 'class_id': i, 'subject': sub})
    #file_names에는 전체 폴더의 jpg파일들 다 들어감 
    assert (len(file_names) == 13233), "Number of files is: {}!".format(len(file_names))
    
    #전체 jpg파일 항목 별로 나누기 
    samples = []
    for item in file_names:
        filename = item['filename']
        class_id = item['class_id']
        sub = item['subject']
        
        #mtcnn으로 crop 
        is_valid, bounding_boxes, landmarks = get_central_face_attributes(filename)

        #crop된 이미지로 다시 file 레이블 만들기 
        if is_valid:
            samples.append(#file_names ->samples
                {'class_id': class_id, 'subject': sub, 'full_path': filename, 'bounding_boxes': bounding_boxes,
                 'landmarks': landmarks})
    #pickle파일로 재저장 
    with open(lfw_pickle, 'wb') as file:
        save = {
            'samples': samples
        }
        pickle.dump(save, file, pickle.HIGHEST_PROTOCOL)


def get_image(samples, transformer, file):
    filtered = [sample for sample in samples if file in sample['full_path'].replace('\\', '/')]
    assert (len(filtered) == 1), 'len(filtered): {} file:{}'.format(len(filtered), file)
    sample = filtered[0]
    full_path = sample['full_path']
    landmarks = sample['landmarks']
    img = align_face(full_path, landmarks)  # BGR
    img = img[..., ::-1]  # RGB
    img = Image.fromarray(img, 'RGB')  # RGB
    img = transformer(img)
    img = img.to(device)
    return img

#Evaluatetraining model
def evaluate(model):
    model.eval()
    #process에서 저장한 pickle 파일열기 
    with open(lfw_pickle, 'rb') as file:
        data = pickle.load(file)
    #'samples'={class_id,subject,file_path,bounding_boxes,landmarks}
    samples = data['samples']
    #positive negative열기 
    filename = 'data/lfw_test_pair.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()

    transformer = data_transforms['val']

    angles = []

    start = time.time()
    with torch.no_grad():
        for line in lines:
            tokens = line.split()
            #anchor image 불러오기 
            file0 = tokens[0]
            img0 = get_image(samples, transformer, file0)
            #positive or negative 불러오기 
            file1 = tokens[1]
            img1 = get_image(samples, transformer, file1)
            #이미지 합치기 
            imgs = torch.zeros([2, 3, 112, 112], dtype=torch.float)
            imgs=imgs.to(device)
            imgs[0] = img0
            imgs[1] = img1
            #cnn feature values 얻기 
            output = model(imgs)
            #feature values 각 배분 
            feature0 = output[0].cpu().numpy()
            feature1 = output[1].cpu().numpy()
            #arcface 분류 
            x0 = feature0 / np.linalg.norm(feature0)
            x1 = feature1 / np.linalg.norm(feature1)
            cosine = np.dot(x0, x1)
            theta = math.acos(cosine)
            theta = theta * 180 / math.pi
            is_same = tokens[2]
            angles.append('{} {}\n'.format(theta, is_same))

    elapsed_time = time.time() - start
    print('elapsed time(sec) per image: {}'.format(elapsed_time / (6000 * 2)))
    #txt 쌍 별 각도 작성 
    with open('data/angles.txt', 'w') as file:
        file.writelines(angles)


def visualize(threshold):
    with open(angles_file) as file:
        lines = file.readlines()

    ones = []
    zeros = []

    for line in lines:
        tokens = line.split()
        angle = float(tokens[0])
        type = int(tokens[1])
        if type == 1:
            ones.append(angle)
        else:
            zeros.append(angle)

    bins = np.linspace(0, 180, 181)

    plt.hist(zeros, bins, density=True, alpha=0.5, label='0', facecolor='red')
    plt.hist(ones, bins, density=True, alpha=0.5, label='1', facecolor='blue')

    mu_0 = np.mean(zeros)
    sigma_0 = np.std(zeros)
    y_0 = scipy.stats.norm.pdf(bins, mu_0, sigma_0)
    plt.plot(bins, y_0, 'r--')
    mu_1 = np.mean(ones)
    sigma_1 = np.std(ones)
    y_1 = scipy.stats.norm.pdf(bins, mu_1, sigma_1)
    plt.plot(bins, y_1, 'b--')
    plt.xlabel('theta')
    plt.ylabel('theta j Distribution')
    plt.title(
        r'Histogram : mu_0={:.4f},sigma_0={:.4f}, mu_1={:.4f},sigma_1={:.4f}'.format(mu_0, sigma_0, mu_1, sigma_1))

    plt.legend(loc='upper right')
    plt.plot([threshold, threshold], [0, 0.05], 'k-', lw=2)
    plt.savefig('images/theta_dist.png')
    plt.show()


def accuracy(threshold):
    with open(angles_file) as file:
        lines = file.readlines()

    wrong = 0
    for line in lines:
        tokens = line.split()
        angle = float(tokens[0])
        type = int(tokens[1])
        if type == 1:
            if angle > threshold:
                wrong += 1
        else:
            if angle <= threshold:
                wrong += 1

    accuracy = 1 - wrong / 6000
    return accuracy

#Show face crop image
def show_bboxes(folder):
    with open(lfw_pickle, 'rb') as file:
        data = pickle.load(file)

    samples = data['samples']
    for sample in tqdm(samples):
        full_path = sample['full_path']
        bounding_boxes = sample['bounding_boxes']
        landmarks = sample['landmarks']
        img = cv.imread(full_path)
        img = draw_bboxes(img, bounding_boxes, landmarks)
        filename = os.path.basename(full_path)
        filename = os.path.join(folder, filename)
        cv.imwrite(filename, img)

#negative<->postive 이미지 분석
def error_analysis(threshold):
    with open(angles_file) as file:
        angle_lines = file.readlines()

    fp = []
    fn = []
    for i, line in enumerate(angle_lines):
        tokens = line.split()
        angle = float(tokens[0])
        type = int(tokens[1])
        if angle <= threshold and type == 0:
            fp.append(i)
        if angle > threshold and type == 1:
            fn.append(i)

    print('len(fp): ' + str(len(fp)))
    print('len(fn): ' + str(len(fn)))

    num_fp = len(fp)
    num_fn = len(fn)

    filename = 'data/lfw_test_pair.txt'
    with open(filename, 'r') as file:
        pair_lines = file.readlines()

    for i in range(num_fp):
        fp_id = fp[i]
        fp_line = pair_lines[fp_id]
        tokens = fp_line.split()
        file0 = tokens[0]
        copy_file(file0, '{}_fp_0.jpg'.format(i))
        save_aligned(file0, '{}_fp_0_aligned.jpg'.format(i))
        file1 = tokens[1]
        copy_file(file1, '{}_fp_1.jpg'.format(i))
        save_aligned(file1, '{}_fp_1_aligned.jpg'.format(i))

    for i in range(num_fn):
        fn_id = fn[i]
        fn_line = pair_lines[fn_id]
        tokens = fn_line.split()
        file0 = tokens[0]
        copy_file(file0, '{}_fn_0.jpg'.format(i))
        save_aligned(file0, '{}_fn_0_aligned.jpg'.format(i))
        file1 = tokens[1]
        copy_file(file1, '{}_fn_1.jpg'.format(i))
        save_aligned(file1, '{}_fn_1_aligned.jpg'.format(i))


def save_aligned(old_fn, new_fn):
    old_fn = os.path.join('data/lfw_funneled', old_fn)
    is_valid, bounding_boxes, landmarks = get_central_face_attributes(old_fn)
    img = align_face(old_fn, landmarks)
    new_fn = os.path.join('images', new_fn)
    cv.imwrite(new_fn, img)


def copy_file(old, new):
    old_fn = os.path.join('data/lfw_funneled', old)
    img = cv.imread(old_fn)
    bounding_boxes, landmarks = get_all_face_attributes(old_fn)
    draw_bboxes(img, bounding_boxes, landmarks)
    cv.resize(img, (224, 224))
    new_fn = os.path.join('images', new)
    cv.imwrite(new_fn, img)

#적절한 thereshold value 얻기 
def get_threshold():

    with open(angles_file, 'r') as file:
        lines = file.readlines()

    data = []

    for line in lines:
        tokens = line.split()
        angle = float(tokens[0])
        type = int(tokens[1])
        data.append({'angle': angle, 'type': type})

    min_error = 6000
    min_threshold = 0

    for d in data:
        threshold = d['angle']
        type1 = len([s for s in data if s['angle'] <= threshold and s['type'] == 0])
        type2 = len([s for s in data if s['angle'] > threshold and s['type'] == 1])
        num_errors = type1 + type2
        if num_errors < min_error:
            min_error = num_errors
            min_threshold = threshold

    # print(min_error, min_threshold)

    return min_threshold

#Test learning model using LFW DATASET 
def lfw_test(model):
    filename = 'data/lfw-funneled.tgz'
    if not os.path.isdir('data/lfw_funneled'):
        print('Extracting {}...'.format(filename))
        extract(filename)

    # if not os.path.isfile(lfw_pickle):
    print('Processing {}...'.format(lfw_pickle))
    process()

    # if not os.path.isfile(angles_file):
    print('Evaluating {}...'.format(angles_file))
    evaluate(model)

    print('Calculating threshold...')
    # threshold = 70.36
    thres = get_threshold()
    with open('data/thereshold.txt', 'w') as file:
        file.write(str(thres))
    print('Calculating accuracy...')
    acc = accuracy(thres)
    print('Accuracy: {}%, threshold: {}'.format(acc * 100, thres))
    return acc, thres


if __name__ == "__main__":
    checkpoint = 'BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model']
    model = model.to(device)
    model.eval()

    acc, threshold = lfw_test(model)

    print('Visualizing {}...'.format(angles_file))
    visualize(threshold)

    print('error analysis...')
    error_analysis(threshold)
