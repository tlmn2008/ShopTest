
from ..common.base_functions import BaseFunctions
from ..common.logger import setup_logger
from ..conf import conf


class Base(object):

    @classmethod
    def setup_class(cls):
        cls.logger = setup_logger('logger', './xunshop_test.log')
        cls.instance = BaseFunctions(cls.logger)
        # cls.instance.mo.clean_db()
        cls.instance.login_by_password(conf.MOBILE_NUMBER, conf.MOBILE_PASSWORD)
        cls.instance.bo.get_url(conf.CATE_URL)

    def setup(self):
        pass

    def teardown(self):
        pass

