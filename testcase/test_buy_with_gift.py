# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *


class TestBuyWithGift(base.Base):
    # 测试满赠营销

    @classmethod
    def setup_class(cls):
        super(TestBuyWithGift, cls).setup_class()

    def test_reach_price_gift(self):
        # 满价格赠
        price = calc_expected_price(conf.GOODS7, 1)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS7, 1, price)
        order_code = self.instance.mo.query_latest_order_code_of_user(conf.MOBILE_NUMBER)
        assert self.instance.mo.check_gift_in_latest_order(order_code, conf.GOODS7['gift'][0], conf.GOODS7['gift_num'][0])

    def test_reach_number_gift(self):
        # 满数量赠
        price = calc_expected_price(conf.GOODS8, 2)
        self.instance.search_and_buy_goods_without_coupon(conf.GOODS8, 2, price)
        order_code = self.instance.mo.query_latest_order_code_of_user(conf.MOBILE_NUMBER)
        assert self.instance.mo.check_gift_in_latest_order(order_code, conf.GOODS8['gift'][0], conf.GOODS8['gift_num'][1])

    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()


