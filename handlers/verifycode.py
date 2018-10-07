# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/6 4:56 PM'
"""

from .base import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun import SendTemplateSMS

import logging
import constants
import re
import random


class ImageCodeHandler(BaseHandler):
    """图片验证码"""

    def get(self):
        # 获取前端传回来的图片验证码编号
        pre_code_id = self.get_argument("p")
        cur_code_id = self.get_argument("c")
        # 生成图片验证码
        # name:图片验证码名称
        # text:图片验证码文本
        # image:图片验证码二进制数据
        name, text, image = captcha.generate_captcha()
        if pre_code_id:
            try:
                self.redis.delete("image_code_{}".format(pre_code_id))
            except Exception as e:
                logging.error(e)
        try:
            self.redis.setex("image_code_{}".format(cur_code_id), constants.IMAGE_CODE_VALIDITY, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type", "image/jpg")
            self.write(image)


class SMSCodeHandler(BaseHandler):
    """手机验证码"""

    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        image_code = self.json_args.get("code")
        image_code_id = self.json_args.get("codeId")

        # 参数校验
        if not all([mobile, image_code, image_code_id]):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})

        # 手机号格式验证
        if not re.match(r"^1\d{10}$", mobile):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})

        # 验证图片验证码
        try:
            # 查询redis获取真实的图片验证码
            real_image_code = self.redis.get("image_code_{}".format(image_code_id))
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "查询redis出错"})

        # 判断验证码是否过期
        if not real_image_code:
            return self.write({"errno": RET.PARAMERR, "errmsg": "图片验证码过期"})

        # 删除redis中的图片验证码
        try:
            self.redis.delete("image_code_{}".format(image_code_id))
        except Exception as e:
            logging.error(e)

        # 判断验证码是否正确
        if not isinstance(image_code, str):
            image_code = str(image_code)
        if not isinstance(real_image_code, str):
            real_image_code = str(real_image_code)
        if image_code.lower() != real_image_code.lower():
            return self.write({"errno": RET.PARAMERR, "errmsg": "图片验证码错误"})

        # 判断手机号是否注册过
        try:
            sql = "select count(*) counts from ih_user_profile where up_mobile=%(mobile)s"
            res = self.db.get(sql, mobile=mobile)
        except Exception as e:
            logging.error(e)
        else:
            if res['counts'] != 0:
                return self.write({"errno": RET.DATAEXIST, "errmsg": "该手机号已存在"})

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 1000000)

        # 在redis中保存短信验证码
        try:
            self.redis.setex("SMSCode" + mobile, constants.SMS_CODE_VALIDITY, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="保存验证码错误"))

        # 发送短信验证码
        try:
            result = SendTemplateSMS.ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_VALIDITY], 1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送短信失败"))

        if result == "000000":
            return self.write(dict(errno=RET.OK, errmsg="发送成功"))
        else:
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送出现错误"))
