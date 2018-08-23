# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *


class TestBuyWithoutDiscounts(base.Base):
    # 测试没有优惠购买

    @classmethod
    def setup_class(cls):
        super(TestBuyWithoutDiscounts, cls).setup_class()

    def test_direct_buy(self):
        price = calc_expected_price(conf.GOODS1, 3)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS1, 3, price)

    def test_return_unpaid_order(self):
        self.instance.cancel_1st_unpaid_order(conf.MOBILE_NUMBER)

    def test_cart_buy(self):
        self.instance.search_and_buy_from_cart(conf.GOODS1)

    def test_cart_buy_multi_goods(self):
        price = calc_expected_price(conf.GOODS1, 2) + calc_expected_price(conf.GOODS13, 3)
        self.instance.search_and_buy_from_cart_multi([conf.GOODS1, conf.GOODS13], [2, 3], price)

    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()


