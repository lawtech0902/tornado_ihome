# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/7 9:43 PM'
"""

from .base import BaseHandler
from utils.response_code import RET
from utils.common import login_required
from utils.image_storage import storage
from config import image_url_prefix

import logging


class ProfileHandler(BaseHandler):
    """个人信息"""

    @login_required
    def get(self):
        """获取个人信息"""
        user_id = self.session.data["user_id"]

        # 查询数据库获取信息
        try:
            sql = "select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s"
            res = self.db.get(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "no data"})

        # 将头像的url地址补充完整
        if res["up_avatar"]:
            img_url = image_url_prefix + res["up_avatar"]
        else:
            img_url = None
        self.write({"errno": RET.OK, "errmsg": "OK", "data": {"user_id": user_id, "name": res["up_name"],
                                                              "mobile": res["up_mobile"], "avatar": img_url}})


class AvatarHandler(BaseHandler):
    """头像"""

    @login_required
    def post(self):
        user_id = self.session.data["user_id"]

        # 获取头像数据，返回一个列表
        avatar = self.request.files.get("avatar")
        if not avatar:
            return self.write(dict(errno=RET.PARAMERR, errmsg="未传头像"))
        try:
            img_name = storage(avatar[0].body)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="上传头像失败"))

        # 操作数据库，保存头像信息
        sql = "update ih_user_profile set up_avatar=%s where up_user_id=%s"
        try:
            self.db.execute_rowcount(sql, img_name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "upload failed"})

        img_url = image_url_prefix + img_name
        self.write({"errno": RET.OK, "errmsg": "OK", "url": img_url})


class NameHandler(BaseHandler):
    """用户名"""

    @login_required
    def post(self):
        # 从session中获取用户身份
        user_id = self.session.data["user_id"]
        name = self.json_args.get("name")

        # 判断name是否传了，并且不应为空字符串
        if name in (None, ""):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})

        # 保存用户name，并同时判断name是否重复（利用db的唯一索引）
        try:
            sql = "update ih_user_profile set up_name=%s where up_user_id=%s"
            self.db.execute_rowcount(sql, name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "用户名已存在"})

        # 修改session中的name字段，并保存到redis中
        self.session.data["name"] = name
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errno": RET.OK, "errmsg": "OK"})


class AuthHandler(BaseHandler):
    """实名认证"""

    @login_required
    def get(self):
        """获取用户实名认证的信息"""
        user_id = self.session.data["user_id"]

        try:
            sql = "select up_real_name,up_id_card from ih_user_profile where up_user_id=%s"
            res = self.db.get(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "获取数据失败"})
        if not res:
            return self.write({"errno": RET.NODATA, "errmsg": "没有数据"})
        self.write({"errno": RET.OK, "errmsg": "OK", "data": {"real_name": res.get("up_real_name", ""),
                                                              "id_card": res.get("up_id_card", "")}})

    @login_required
    def post(self):
        """保存实名认证信息"""
        user_id = self.session.data["user_id"]
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")

        # 参数校验
        if real_name in (None, "") or id_card in (None, ""):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})
        try:
            sql = "update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s"
            self.db.execute_rowcount(sql, real_name, id_card, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "更新失败"})
        self.write({"errno": RET.OK, "errmsg": "OK"})
