# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 4:04 PM'
"""

from handlers import passport

handlers = [
    (r"/", passport.IndexHandler),
]
