__author__ = 'jfang'

import requests

import qiniu
from qiniu import *

access_key = 'dbPhcCoD5oQKeaIays_NkoYVsNwQ-kuzEzuI-whv'
secret_key = 'gbIZYLlYMkkrm55u2p7TXsL_Qx942q8lY_3gEHcG'
bucket_name = 'fanfan-photo'


q = Auth(access_key, secret_key)

private_key = '285407715624'
base_url = 'http://%s/%s' % (bucket_name+'.7te7w9.com1.z0.glb.clouddn.com', private_key)
private_url = q.private_download_url(base_url, expires=3600)
print(private_url)
r = requests.get(private_url)
print(r)

