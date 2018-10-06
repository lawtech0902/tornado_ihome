# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 3:59 PM'
"""

from tornado.options import define, options
from urls import handlers

import config
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import torndb
import redis

define("port", type=int, default=8000, help="run server on the given port")


class Application(tornado.web.Application):
    """定制的Application，用来补充db数据库实例"""

    def __init__(self, *args, **kwargs):
        # 调用执行父类tornado.web.Application的初始化方法
        super(Application, self).__init__(*args, **kwargs)

        # 构造数据库连接对象
        self.db = torndb.Connection(**config.mysql_options)

        # 构造redis连接实例
        self.redis = redis.StrictRedis(**config.redis_options)


def main():
    # 设置日志文件保存目录
    options.log_file_prefix = config.log_path
    # 设置日志输出等级
    options.logging = config.log_level
    # 设置日志文件切割大小
    # options.log_file_max_size = 128

    # 转换命令行参数
    tornado.options.parse_command_line()
    app = Application(handlers, **config.settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
