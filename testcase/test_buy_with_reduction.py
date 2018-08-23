# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *


class TestBuyWithReduction(base.Base):
    # 测试满减营销

    @classmethod
    def setup_class(cls):
        super(TestBuyWithReduction, cls).setup_class()

    def test_reach_price_reduction(self):
        # 满价格减
        price = calc_expected_price(conf.GOODS3, 3)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS3, 3, price)

    def test_reach_number_reduction(self):
        # 满数量减
        price = calc_expected_price(conf.GOODS4, 2)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS4, 2, price)



    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()


