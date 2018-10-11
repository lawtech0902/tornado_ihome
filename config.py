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
    "xsrf_cookies": True,
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

# 日志文件
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

# 日志等级
log_level = "debug"

# 密码加密密钥
passwd_hash_key = "F3fv87mzTI6fKbP13gUNZI+eZrL1VEzguyX1+AVsRdI="

# 七牛空间域名
image_url_prefix = "http://pg8dp3e10.bkt.clouddn.com/"
