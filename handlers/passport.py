# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/5 4:07 PM'
"""

from .base import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import login_required

import config
import re
import logging
import hashlib


class RegisterHandler(BaseHandler):
    """注册"""

    def post(self):
        # 接收参数
        mobile = self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")

        # 校验参数
        if not all([mobile, sms_code, password]):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})
        if not re.match(r"^1\d{10}$", mobile):
            return self.write({"errno": RET.PARAMERR, "errmsg": "手机号码格式错误"})

        # 为方便调试，不用每次发短信，留一个万能验证码
        if sms_code != "2468":
            try:
                real_code = self.redis.get("SMSCode" + mobile)
            except Exception as e:
                logging.error(e)
                return self.write({"errno": RET.DBERR, "errmsg": "读取验证码异常"})

            # 判断验证码是否过期
            if not real_code:
                return self.write({"errno": RET.PARAMERR, "errmsg": "验证码过期"})

            # 判断验证码是否正确
            if real_code != str(sms_code):
                return self.write({"errno": RET.PARAMERR, "errmsg": "验证码无效"})

            # 删除redis中的smscode
            try:
                self.redis.delete("SMSCode" + mobile)
            except Exception as e:
                logging.error(e)

        # 操作数据库，保存用户信息
        # 加密密码
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        sql = "insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)"
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile, password=password)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DATAEXIST, "errmsg": "手机号已注册"})
        # session操作
        try:
            session = Session(self)
            session.data["user_id"] = user_id
            session.data["name"] = mobile
            session.data["mobile"] = mobile
            session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errno": RET.OK, "errmsg": "OK"})


class LoginHandler(BaseHandler):
    """登录"""

    def post(self):
        # 接收参数
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")

        # 检查参数
        if not all([mobile, password]):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})
        if not re.match(r"^1\d{10}$", mobile):
            return self.write({"errno": RET.PARAMERR, "errmsg": "手机号码格式错误"})

        # 检验密码
        sql = "select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s"
        res = self.db.get(sql, mobile=mobile)
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        if res and res["up_password"] == password:
            try:
                session = Session(self)
                session.data["user_id"] = res["up_user_id"]
                session.data["name"] = res["up_name"]
                session.data["mobile"] = mobile
                session.save()
            except Exception as e:
                logging.error(e)
            return self.write({"errno": RET.OK, "errmsg": "OK"})
        else:
            return self.write({"errno": RET.DATAERR, "errmsg": "手机号或密码错误"})


class CheckLoginHandler(BaseHandler):
    """检查登录状态"""

    def get(self):
        # get_current_user方法在基类中已实现
        # 若用户登录过，返回用户昵称，否则返回None
        user_name = self.get_current_user()
        if user_name:
            self.write({"errno": RET.OK, "errmsg": "true", "data": {"name": user_name}})
        else:
            self.write({"errno": RET.SESSIONERR, "errmsg": "false"})


class LogoutHandler(BaseHandler):
    """登出"""

    @login_required
    def get(self):
        # 清除session数据
        self.session.clear()
        self.write({"errno": 0, "errmsg": "OK"})
