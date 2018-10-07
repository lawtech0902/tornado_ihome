# _*_ coding: utf-8 _*_
"""
__author__ = 'lawtech'
__date__ = '2018/10/6 7:48 PM'
"""

# session数据有效期， 单位秒
SESSION_REDIS_EXPIRES = 86400

# 图片验证码有效期 秒
IMAGE_CODE_VALIDITY = 120

# 短信验证码有效期 秒
SMS_CODE_VALIDITY = 300

# 主页房屋展示最大数量
HOME_PAGE_MAX_HOUSES = 5

# 主页缓存数据过期时间 秒
HOME_PAGE_DATA_REDIS_EXPIRE_SECOND = 7200

# 城区信息缓存时间 秒
AREA_INFO_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页每页数目
HOUSE_LIST_PAGE_CAPACITY = 3

# redis每次缓存房屋列表页数
HOUSE_LIST_REDIS_CACHED_PAGE = 2

# 房屋列表缓存时间 秒
HOUSE_LIST_REDIS_EXPIRE_SECOND = 3600

# 房屋详情缓存时间 秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋详情页评论显示个数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30
