# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
from time import sleep


class MySqlOperator(object):
    dbhost = 'xunshop-test02.cukma1tn2ioi.rds.cn-north-1.amazonaws.com.cn'
    dbuser = 'xiaoxun'
    dbpasswd = 'xiaoxun2018!'
    dbname = 'xunshop'

    def __init__(self, logger):
        self.logger = logger
        try:
            self.conn = MySQLdb.connect(self.dbhost, self.dbuser, self.dbpasswd, self.dbname, charset='utf8')
            self.cursor = self.conn.cursor()
        except MySQLdb.Error, e:
            self.logger.error("Init MysqlDB failed, ERROR is {}".format(str(e)))


    def execute(self, cmd):
        try:
            self.cursor.execute(cmd)
            self.conn.commit()
        except MySQLdb.Error, e:
            self.logger.error("Execute SQL failed, ERROR is {}".format(str(e)))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

    def query_latest_order_code_of_user(self, username):

        sql = ' select order_code from np_order a, np_customer b where a.customer_id = b.customer_id and ' \
              'b.customer_username = "{}" and a.order_status = "0" order by order_code desc limit 1;'.format(username)
        result = self.execute(sql)
        if not result:
            self.logger.error("Get None result for SQL: {}".format(sql))
            return None
        result = result[0][0]
        return result

    def query_order_id_from_order_code(self, order_code):
        sql = "select order_id from np_order where order_code = {}".format(order_code)
        result = self.execute(sql)
        if not result:
            self.logger.error("Get None result for SQL: {}".format(sql))
            return None
        result = result[0][0]
        return result

    def query_order_status(self, order_code):
        sql = "select order_status from np_order where order_code = {};".format(order_code)

        result = self.execute(sql)
        self.logger.info("origin result: {}".format(result))
        if result:
            result = result[0][0]
        sleep(1)
        if not result:
            return result
        else:
            return int(result)

    def check_order_status(self, order_code, expected_status=None, timeout=10):

        for i in xrange(0, timeout):
            result = self.query_order_status(order_code)
            if result == expected_status:
                return True
        self.logger.error("After {} seconds waiting, the order status is {}, it should be {}".format
                          (timeout, result, expected_status))
        return False

    def check_gift_in_latest_order(self, order_code, gift_name, gift_num):
        # 根据order_code检查是否赠送了指定数量的赔品
        order_id = self.query_order_id_from_order_code(order_code)
        # 获取礼品数量
        sql = "select nog.goods_info_num from np_order_goods nog, np_goods ng " \
              "where nog.order_id = {} and nog.goods_id = ng.goods_id and ng.goods_name =\"{}\";".format(order_id, gift_name)
        result = self.execute(sql)
        if not result:
            self.logger.error("Get None result for SQL: {}".format(sql))
            return False
        result = result[0][0]

        if int(result) != gift_num:
            self.logger.error("Gift number {} is incorrect, it should be {}".format(result, gift_num))
            return False
        return True

    def clean_db(self):

        # 清空所有人的购物车
        clean_cart = 'delete from np_shopping_cart;'
        # clean_cart = 'delete nsc from np_shopping_cart nsc, np_customer nc where nsc.customer_id = nc.customer_id and nc.customer_username = username;'

        # 清空被领取的优惠券
        clean_coupon = 'update qm_coupon_code set customer_id = NULL, acquire_time = NULL, use_status = 0, use_date = NULL, order_code = NULL;'

        # 清空所有订单(暂不执行)
        clean_order = 'delete from np_order_goods; delete from np_order; delete from np_order_express;'

        self.execute(clean_cart)
        self.execute(clean_coupon)
