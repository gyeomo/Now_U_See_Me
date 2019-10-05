import requests
import os

path_dir = './test_img/'
url = 'http://203.252.91.45:3000/event/uploady'

filename_list = os.listdir(path_dir) # 

print(filename_list) # debug log
filename_list.remove('.DS_Store') #

file_list = []

# 
for each in filename_list:
    file_obj = []
    file_obj.append('file')
    file_obj.append(open(path_dir+each, 'rb'))
    file = tuple(file_obj)
    file_list.append(file)

print(file_list)


res = requests.post(url, files = file_list)
print(res)

# #test
# res = requests.get('http://127.0.0.1:3000/users')
# print(res)
