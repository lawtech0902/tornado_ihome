# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 4:04 PM'
"""

from handlers import passport
from handlers import verifycode
from tornado.web import StaticFileHandler

import os

ihome_api_urls = [
    # 用户管理功能部分
    (r"/", passport.IndexHandler),
    (r"/api/imagecode", verifycode.ImageCodeHandler),   # 图片验证码
    (r"/api/smscode", verifycode.SMSCodeHandler),   # 短信验证码
]

urls = []
urls.extend(ihome_api_urls)
urls.extend([
    (r"^/(.*?)$", StaticFileHandler,
     {"path": os.path.join(os.path.dirname(__file__), "html"), "default_filename": "index.html"}
     ),
])
