# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 4:07 PM'
"""

from .base import BaseHandler


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write("Hello, world!")
