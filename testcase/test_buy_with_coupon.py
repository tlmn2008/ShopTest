# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *


class TestBuyWithCoupon(base.Base):
    # 测试优惠券活动

    @classmethod
    def setup_class(cls):
        super(TestBuyWithCoupon, cls).setup_class()

    def test_coupon(self):
        self.instance.mo.clean_db()
        buy_amount = 1
        price = calc_expected_price(conf.GOODS12, buy_amount)
        self.instance.search_and_view_goods(conf.GOODS12['name'])
        # 领取优惠券
        self.instance.pick_coupon()
        # 领取完成回退到商品页
        self.instance.bo.go_back()
        self.instance.buy_goods_with_coupon(conf.GOODS12['params'], buy_amount, price)

    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()

