# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/7 10:13 PM'
"""

import logging

from qiniu import Auth, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'HoVf_G8_5f5PoKoWLozK_eRZdhN0iD4SHdJzJaRQ'
secret_key = 'ja1fPapNAFLVu2ZC8oX1gbjef8NIySwqJKHS4Jgb'

# 要上传的空间
bucket_name = 'ihome'


def storage(data):
    """七牛云存储上传文件接口"""
    if not data:
        return None
    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name)

        # 上传文件
        ret, info = put_data(token, None, data)

    except Exception as e:
        logging.error(e)
        raise e

    if info and info.status_code != 200:
        raise Exception("上传文件到七牛失败")

    return ret["key"]


if __name__ == '__main__':
    file_name = input("输入上传的文件")
    with open(file_name, "rb") as f:
        storage(f.read())
