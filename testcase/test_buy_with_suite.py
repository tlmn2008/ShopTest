# encoding: utf-8
from . import base
from ..conf import conf, boss, mobile
from ..common.utility import *

class TestBuyWithSuite(base.Base):
    # 测试套装营销

    @classmethod
    def setup_class(cls):
        super(TestBuyWithSuite, cls).setup_class()

    def test_buy_suite(self):

        price = calc_expected_price(conf.GOODS2, 1)
        self.instance.search_and_add_suite_to_cart(conf.GOODS2)
        self.instance.buy_suite_from_cart(price)

    @classmethod
    def teardown_class(cls):
        cls.instance.bo.close()


