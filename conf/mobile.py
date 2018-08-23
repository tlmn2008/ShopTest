# -*- coding: utf-8 -*-
# elements of mobile pages

# Element ID
ID_SEARCH_INPUT = 'searchInput'    # 搜索条
ID_SEARCH_BTN = 'search_btn'       # 搜索按钮
ID_ORDER_PRICE = 'summary_order_amount'    # 付款页总额

ID_MOBILE_NUMBER = 'mobile'         # 登录页面手机号输入框
ID_AUTH_CODE = 'code'               # 登录页面验证码输入框

ID_USER_NAME = 'log_user'           # 账户密码登录页面的用户名输入框
ID_USER_PASSWD = 'log_psd'          # 账户密码登录页面的密码输入框

ID_USE_COUPON = 'use_coupon_result'    # 订单页优惠券‘去使用’

ID_CONFIRM_COUPON = 'saveCoupon'        # 订单页选择优惠券后的确认按钮
ID_ADD_CART_CONFIRM = 'add_cart'        # 加入购物车，选择型号和数量后的'确定'按钮

ID_PAY_ORDER_PRICE = 'order'         # 选择支付方式页面的待支付金额

# CSS
CSS_MENU = 'icon-caidan'
CSS_MINE = 'icon-wode'
CSS_MAIN = 'icon-shouye2'
CSS_CATEGORY = 'xx-cates'

CSS_UNPAID = 'icon-daifukuan'       # '我的'页面待付款按钮
CSS_CONFIRM = 'ui-dialog-autofocus'  # 取消订单的确认按钮

CSS_GET_COUPON = 'label-coupons'     # 商品页的领券按钮

CSS_INCREASE_AMOUNT = 'num_plus'    # 商品页点'立即购买'后的数量加号按钮
CSS_CART = 'icon iconfont icon-cart'    # 商品页的‘购物车’按钮，进入购物车
CSS_SETTLE = 'settle-btn'               # 购物车中的'结算'按钮

# xpath
LOGIN_NAME_INPUT = '//*[@id="mobile"]'
LOGIN_PASSWORD_INPUT = '//*[@id="code"]'
LOGIN_BUTTON = '/html/body/div[1]/div[3]/a'

# 优惠券领取页的第一张券
XPATH_COUPON1 = '/html/body/div/div/div/div/ul/li/div/a'
# 优惠券领取页的第二张券
XPATH_COUPON2 = '/html/body/div/div/div/div/ul/li[2]/div/a'
# 订单页选中第一张优惠券
XPATH_SELECT_COUPON1 = '/html/body/div/div[6]/div/div[2]/div/ul/li/div/label/div/i'
# 订单页选中第二张优惠券
XPATH_SELECT_COUPON2 = '/html/body/div/div[6]/div/div[2]/div/ul/li[2]/div/label/div/i'

XPATH_SEARCH_BUTTON = '//*[@id="search_btn"]'     # 搜索按钮
XPATH_CART = '//span[contains(text(), "购物车")]'      # 商品页的'购物车'按钮
XPATH_SELECT_ALL_CHECKBOX_IN_CART = '//span[contains(text(), "平台自营")]'  # 购物车中点击‘平台自营’前的check box
XPATH_SELECT_SUITE1_IN_CART = '//div[@class="suit-head"]/label[1]'          # 购物车中点击第一个套装的check box, 即选中它
XPATH_LOGIN = '//a[@class="btn btn-full div_login login_part"]'     # 使用账号密码登录页面的确认按钮

# text
TEXT_MAIN = u'首页'      # 首页
TEXT_CATEGORY = u'分类'         # 分类
TEXT_CART = u'购物车'             # 购物车
TEXT_MINE = u'我的'             # 我的
TEXT_CONFIRM = u'确认'
TEXT_LOGIN = u'登 录'           # 登录页面登录按钮
TEXT_PASSWD_LOGIN = u'账号密码登录'   # 登录页面选择账号密码登录
TEXT_CANCEL_ORDER = u'取消订单'  # 订单页面取消订单按钮

TEXT_CUSTOMER_SERVICE = u'客服'        # 客服
TEXT_FAVORITE = u'收藏'                # 收藏
TEXT_ADD_CART = u'加入购物车'                 # 加入购物车
TEXT_BUY = u'立即购买'                         # 立即购买
TEXT_COMMIT = u'提交订单'
TEXT_COUNT = u'结算'              # 购物车中的'结算'按钮



