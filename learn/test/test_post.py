import client_manager

cm = client_manager.ClientManager()
test_result = {
    'eventTime': '2019-9-30-22-4-24-744577',
    'img_addrs': ['../unknown/2019-9-30-22-4-24-744577/2019-9-30-22-4-24-744577.jpg',\
        '../unknown/2019-9-30-22-4-24-744577/2019-9-30-22-5-18-15354.jpg',\
        '../unknown/2019-9-30-22-4-24-744577/2019-9-30-22-5-20-588613.jpg'],
    'types': ['unknown','unknown','unknown']
}

res = cm.post_status_unknown(test_result)
print(res.status_code)