# encoding: utf-8

from browser_operator import BrowserOperator
from mysql_operator import MySqlOperator
from ..conf import conf, boss, mobile

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


class BaseFunctions(object):

    def __init__(self, logger):

        # init browser operator
        self.logger = logger
        self.bo = BrowserOperator(self.logger)
        # self.mo = MySqlOperator(self.logger)

    def login_by_sms(self):
        # login by sms code
        self.bo.get_url(conf.LOGIN_URL)
        self.bo.id_input(mobile.ID_MOBILE_NUMBER, conf.MOBILE_NUMBER)
        self.bo.id_input(mobile.ID_AUTH_CODE, conf.MOBILE_SMS_CODE)
        try:
            self.bo.xpath_click(mobile.LOGIN_BUTTON)
        except TimeoutException:
            self.bo.exec_script('window.stop()')

    def login_by_password(self, mobile_number, mobile_passwd):
        # login by username/password
        self.bo.get_url(conf.LOGIN_URL)
        self.bo.text_click(mobile.TEXT_PASSWD_LOGIN)
        self.bo.id_input(mobile.ID_USER_NAME, mobile_number)
        self.bo.id_input(mobile.ID_USER_PASSWD, mobile_passwd)
        self.bo.xpath_click(mobile.XPATH_LOGIN)

    def search_goods(self, goods_name):
        self.bo.id_input(mobile.ID_SEARCH_INPUT, goods_name)
        self.bo.id_input(mobile.ID_SEARCH_INPUT, Keys.ENTER)

    def search_and_view_goods(self, goods_name):
        # 搜索并进入商品
        self.bo.get_url(conf.CATE_URL)
        self.search_goods(goods_name)
        self.bo.id_click(mobile.ID_SEARCH_INPUT)
        self.bo.id_clean(mobile.ID_SEARCH_INPUT)
        # 截取goods_name空格前的商品名称
        goods_name = goods_name.split()[0]
        self.bo.p_text_click(goods_name)

    def choose_coupon(self):
        self.bo.id_click(mobile.ID_USE_COUPON)
        self.bo.xpath_click(mobile.XPATH_SELECT_COUPON1)
        self.bo.id_click(mobile.ID_CONFIRM_COUPON)

    def pick_coupon(self):
        # 商品页面领取优惠券
        # self.bo.id_css_click('activityContainer', 'label-coupons')
        self.bo.class_click(mobile.CSS_GET_COUPON)
        self.bo.xpath_click(mobile.XPATH_COUPON1)

    def select_goods_params(self, params):
        # 选择产品型号
        for param in params:
            self.bo.text_click(param)

    def increase_amount(self, num=1):
        # 提高购买数量，默认1个
        for i in xrange(1, num):
            self.bo.class_click(mobile.CSS_INCREASE_AMOUNT)

    def add_to_cart(self, goods_param, num):
        # 选择产品型号和数量，添加进购物车
        self.bo.text_click(mobile.TEXT_ADD_CART)
        self.select_goods_params(goods_param)
        self.increase_amount(num)
        self.bo.id_click(mobile.ID_ADD_CART_CONFIRM)
    
    def search_and_add_suite_to_cart(self, goods):
        # 查询商品，并把其优惠套装添加进购物车
        self.search_and_view_goods(goods['name'])
        # 展开优惠套装
        self.bo.xpath_click('//span[contains(text(), "特惠套装")]')
        # 进入优惠套装
        self.bo.class_click('prefer_suit_short')
        # 加入购物车
        self.bo.text_click(u'加入购物车')

    def check_order_mount_and_submit_order(self, expected_order_price=None):
        # check the order price
        result = True
        if expected_order_price:
            price = self.bo.id_text(mobile.ID_ORDER_PRICE)
            if float(price) == expected_order_price:
                self.logger.info("The order price is correct!")
            else:
                self.logger.error("The order price {} is incorrect, it should be {}".format(price, expected_order_price))
                result = False

        self.bo.text_click(mobile.TEXT_COMMIT)

        # 下单后检查待支付金额. 从字符 如：' ￥149.00元' 中截取订单金额
        unpaid_price = str(self.bo.id_text(mobile.ID_PAY_ORDER_PRICE))[3:-3]

        if not float(unpaid_price) == expected_order_price:
            self.logger.error("The order price {} in the pay page is incorrect, it should be {}".format(unpaid_price, expected_order_price))
            result = False
        assert result

    def buy_goods_without_coupon(self, goods_param, goods_number=1, expected_order_price=None):
        # 直接购买商品，检查价格并下单
        self.bo.text_click(mobile.TEXT_BUY)
        self.select_goods_params(goods_param)
        self.increase_amount(goods_number)
        self.bo.text_click(mobile.TEXT_CONFIRM)
        self.check_order_mount_and_submit_order(expected_order_price)

    def buy_goods_with_coupon(self, goods_param, goods_number, expected_order_price):
        # 购买商品时使用优惠券，检查价格并下单
        self.bo.text_click(mobile.TEXT_BUY)
        self.select_goods_params(goods_param)
        self.increase_amount(goods_number)
        self.bo.text_click(mobile.TEXT_CONFIRM)
        self.choose_coupon()
        self.check_order_mount_and_submit_order(expected_order_price)

    def search_and_buy_goods_without_coupon(self, goods, goods_number, expected_order_price):
        # 购买，无优惠券，但可能有满减/折等活动
        self.search_and_view_goods(goods['name'])
        self.buy_goods_without_coupon(goods['params'], goods_number, expected_order_price)

    def search_and_buy_goods_with_coupon(self, goods_name, goods_param, goods_number, expected_order_price):
        self.search_and_view_goods(goods_name)
        self.buy_goods_with_coupon(goods_param, goods_number, expected_order_price)

    def enter_cart(self):
        # 进入购物车
        self.bo.get_url(conf.CART_URL)

    def buy_from_cart(self, expected_order_price):
        # 从购物车结算
        self.bo.xpath_click(mobile.XPATH_CART)
        self.bo.class_click(mobile.CSS_SETTLE)
        self.check_order_mount_and_submit_order(expected_order_price)

    def search_and_buy_from_cart(self, goods, num=1):
        self.search_and_view_goods(goods['name'])
        self.add_to_cart(goods['params'], num)
        self.buy_from_cart(goods['price'] * num)

    def search_and_buy_from_cart_multi(self, goods_list, num_list, expected_order_price):
        # 添加多个商品进购物车一起结算
        if len(goods_list) != len(num_list):
            self.logger.error("The length of goods and number are not same.")
            return False

        for i in xrange(len(goods_list)):
            self.search_and_view_goods(goods_list[i]['name'])
            self.add_to_cart(goods_list[i]['params'], num_list[i])
        self.buy_from_cart(expected_order_price)
        
    def buy_suite_from_cart(self, price):
        self.enter_cart()
        # 取消所有勾选
        self.bo.xpath_click(mobile.XPATH_SELECT_ALL_CHECKBOX_IN_CART)
        # 勾选第一个优惠套装
        self.bo.xpath_click(mobile.XPATH_SELECT_SUITE1_IN_CART)
        # 进入结算页面
        self.bo.p_text_click(mobile.TEXT_COUNT)     
        self.check_order_mount_and_submit_order(price)

    def cancel_1st_unpaid_order(self, username):

        self.bo.get_url(conf.MINE_URL)
        self.bo.class_click(mobile.CSS_UNPAID)
        order_code = self.mo.query_latest_order_code_of_user(username)
        order_code_div = "div{}".format(order_code)
        self.bo.id_text_click(order_code_div, mobile.TEXT_CANCEL_ORDER)
        self.bo.class_click(mobile.CSS_CONFIRM)

        # check order is canceled in DB
        assert self.mo.check_order_status(order_code, 4)

    def close(self):
        self.bo.close()
        # self.mo.close()
