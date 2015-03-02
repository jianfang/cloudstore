__author__ = 'jfang'

import uuid

import qiniu
from qiniu import *

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


access_key = 'dbPhcCoD5oQKeaIays_NkoYVsNwQ-kuzEzuI-whv'
secret_key = 'gbIZYLlYMkkrm55u2p7TXsL_Qx942q8lY_3gEHcG'
bucket_name = 'fanfan-photo'

class QiniuCloud:
    @staticmethod
    def get_download_url(private_key):
        q = Auth(access_key, secret_key)
        base_url = 'http://%s/%s' % (bucket_name+'.7te7w9.com1.z0.glb.clouddn.com', private_key)
        private_url = q.private_download_url(base_url, expires=3600)
        #print(private_url)
        return private_url

    @staticmethod
    def get_upload_token(key):
        q = Auth(access_key, secret_key)
        return q.upload_token(bucket_name, key)

    @staticmethod
    def get_unique_filename():
        unique_filename = str(hash(uuid.uuid4()) % 1000000000000) # 1T
        print(unique_filename)
        return unique_filename


if __name__ == "__main__":
    localfile = __file__
    key = QiniuCloud.get_unique_filename()
    mime_type = "text/plain"
    #params = {'x:a': 'a'}

    token = QiniuCloud.get_upload_token(key)
    ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


