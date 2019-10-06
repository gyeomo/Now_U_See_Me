import os

import zipfile

#Unpack the images zip file 
def extract(filename):
    print('Extracting {}...'.format(filename))
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall('data')
    zip_ref.close()

if __name__ == "__main__":
    if not os.path.isdir('data/faces_glintasia'): #images zip file name
        extract('data/faces_glintasia.zip')
