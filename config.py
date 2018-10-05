# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 4:07 PM'
"""

import os

# Application类用到的配置参数
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "html"),
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    "cookie_secret": "IZP7O8ghT8esP1Fy6S8FKt9fsqaTgUzMj0CjFAkGom8=",
    "xsrf_cookies": "riD95751SQ2HEfMiCXnX7Lj40l3dNk8ohRmkeN+Gf9s=",
    "debug": True,
}

# mysql配置
mysql_options = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "12",
    "database": "ihome"
}

# redis配置
redis_options = {
    "host": "127.0.0.1",
    "port": 6379
}