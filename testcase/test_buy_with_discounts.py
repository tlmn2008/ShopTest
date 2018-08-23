# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *


class TestBuyWithDiscounts(base.Base):
    # 测试满折营销

    @classmethod
    def setup_class(cls):
        super(TestBuyWithDiscounts, cls).setup_class()

    def test_reach_price_discount(self):
        # 满价格折
        price = calc_expected_price(conf.GOODS5, 2)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS5, 2, price)
    #
    # def test_reach_number_discount(self):
    #     # 满数量折
    #     price = calc_expected_price(conf.GOODS6, 3)
    #     self.instance.search_and_buy_goods_without_coupon(conf.GOODS6, 3, price)


    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()


