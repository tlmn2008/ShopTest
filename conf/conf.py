# -*- coding: utf-8 -*-

BOSS_URL = 'http://'
MOBILE_URL = 'http://'
LOGIN_URL = "{}{}".format(MOBILE_URL, 'loginm.html?url=/customercenter.html')
CATE_URL = "{}{}".format(MOBILE_URL, 'cates.html')
CART_URL = "{}{}".format(MOBILE_URL, "myshoppingmcart.html")
MINE_URL = "{}{}".format(MOBILE_URL, 'customercenter.html')

BOSS_ADMIN_NAME = 'admin'
BOSS_ADMIN_PASSWORD = 'abcd1234'

MOBILE_NUMBER = '1760xxxxx'
MOBILE_PASSWORD = 'abcd1234'
MOBILE_SMS_CODE = '123123'


# Test goods info.
# Format: GOODS = {'name': , 'params': , 'price': , 'discounts': }

# 无优惠
GOODS1 = {'name': u'小寻儿童电话手表T1 10天超长待机 ', 'params': [u'天蓝色'], 'price': 399.00, 'reduction': [0], 'discount': None}

# 套装A, 减200
GOODS2 = {'name': u'小寻儿童电话手表T1 10天超长待机 ', 'params': [u'粉橙色'], 'price': 448.00, 'reduction': [0], 'discount': None}

# 满价格减, 399/20, 798/40, 1197/60
GOODS3 = {'name': u'小寻儿童电话手表X1 4G版AI手表', 'params': [u'粉橙色'], 'price': 499.00, 'reduction': [20,40,60], 'discount': None}

# 满数量减, 满2个减100元
GOODS4 = {'name': u'小寻儿童电话手表X1 4G版AI手表', 'params': [u'青绿色'], 'price': 499.00, 'reduction': [0, 100], 'discount': None}

# 满价格折, 满200打5折，满500打2折
GOODS5 = {'name': u'小寻儿童电话手表302彩屏版', 'params': [u'天蓝色'], 'price': 169.00, 'reduction': None, 'discount': [0.5,0.5,0.2]}

# 满数量折, 1个9折，2个8折，3个7折，4个5折
GOODS6 = {'name': u'小寻儿童电话手表302彩屏版', 'params': [u'粉橙色'], 'price': 169.00, 'reduction': None, 'discount': [0.9, 0.8, 0.7,0.5]}

# 满价格赠, 满299赠1个，满500赠2个定位电话
GOODS7 = {'name': u'小寻儿童电话手表S1(天蓝色)', 'params': [u'天蓝色'], 'price': 299.00, 'reduction': [0], 'discount': None, 'gift': [u'小寻米兔GPS定位电话'], 'gift_num': [1,2]}

# 满数量赠, 满1个赠2个，满2个赠4个定位电话
GOODS8 = {'name': u'小寻儿童电话手表S1(天蓝色)', 'params': [u'粉橙色'], 'price': 299.00, 'reduction': [0], 'discount': None,  'gift': [u'小寻米兔GPS定位电话'], 'gift_num': [2,4]}

# 套装A
GOODS9 = {'name': u'小寻儿童电话手表A2 高性价比力荐(天蓝色)', 'params': [u'天蓝色'], 'price': 448.00, 'reduction': [0], 'discount': None}

# 抢购, 5折，限购2个
GOODS10 = {'name': u'小寻儿童电话手表A2 高性价比力荐(天蓝色)', 'params': [u'粉橙色'], 'price': 249.00, 'reduction': None, 'discount': [0.5]}

# 拼团, 2人团，限购2件
GOODS11 = {'name': u'小寻儿童电脑 早教机 学习机器人', 'params': [u'王子蓝'], 'price': 899.00, 'reduction': [100], 'discount': None}

# 优惠券， 满88减10， 共3张
GOODS12 = {'name': u'小寻儿童电脑 原装麦克风', 'params': [u'王子蓝'], 'price': 99.00, 'reduction': [10], 'discount': None}

# 无优惠
GOODS13 = {'name': u'小寻儿童爆米花鞋 夏季款运动鞋', 'params': ['32', u'粉橙色'], 'price': 149.00, 'reduction': [0], 'discount': None}

