__author__ = 'jfang'

import uuid

import qiniu
from qiniu import *

access_key = 'dbPhcCoD5oQKeaIays_NkoYVsNwQ-kuzEzuI-whv'
secret_key = 'gbIZYLlYMkkrm55u2p7TXsL_Qx942q8lY_3gEHcG'

q = Auth(access_key, secret_key)

# 直接上传二进制流

# key = 'a\\b\\c"你好'
# data = 'hello bubby!'
# token = q.upload_token(bucket_name)
# ret, info = put_data(token, key, data)
# print(info)
# assert ret['key'] == key
#
# key = ''
# data = 'hello bubby!'
# token = q.upload_token(bucket_name, key)
# ret, info = put_data(token, key, data, check_crc=True)
# print(info)
# assert ret['key'] == key


# 上传本地文件

def get_upload_token(key):
    bucket_name = 'fanfan-photo'
    return q.upload_token(bucket_name, key)

def get_unique_filename():
    unique_filename = str(hash(uuid.uuid4()) % 1000000000000) # 1T
    print(unique_filename)
    return unique_filename

localfile = __file__
key = get_unique_filename()
mime_type = "text/plain"
#params = {'x:a': 'a'}

token =get_upload_token(key)
ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)


