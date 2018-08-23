# -*- coding: utf-8 -*-
#
# from common.browser_operator import *
# from conf import conf, mobile
# from common.mysql_operator import MySqlOperator
#
# from selenium.common.exceptions import TimeoutException
#
# for i in range(1,2):
#     bo2 = BrowserOperator()
#     # bo2.get_url(conf.mobile_addr)
#
#     # mobile login
#     bo2.get_url(conf.login_url)
#     bo2.xpath_fill_input(mobile.login_name_input, conf.mobile_number)
#     bo2.xpath_fill_input(mobile.login_password_input, conf.mobile_password)
#     try:
#         bo2.xpath_click(mobile.login_button)
#     except TimeoutException:
#         print "catch exception of timeout"
#         bo2.exec_script('window.stop()')
#
#     bo2.class_click(mobile.css_menu)
#     bo2.class_click(mobile.css_category)
#
#     bo2.id_input(mobile.id_search_input, conf.goods1_name)
#
#     bo2.id_input(mobile.id_search_input, Keys.ENTER)
#
#     bo2.id_click(mobile.id_search_input)
#     bo2.id_clean(mobile.id_search_input)
#
#     bo2.text_click(conf.goods1_name)
#
#     bo2.text_click(mobile.buy)
#
#     bo2.text_click(conf.goods1_params)
#
#     bo2.text_click(mobile.confirm)
#     sleep(1)
#
#     price = bo2.id_text(mobile.id_order_price)
#
#     print "order price is {}".format(price)
#
#     if float(price) == conf.goods1_price:
#         print "OK, the price is correct!"
#         bo2.text_click(mobile.commit)
#     else:
#         print "ERROR, the price {} is incorrect, it should be {}".format(price, conf.goods1_price)
#
#     bo2.get_url(conf.mobile_url + "main.html")
#     sleep(1)
#     bo2.get_url(conf.mobile_url + "customercenter.html")
#
#     bo2.class_click(mobile.css_unpaid)
#     sleep(1)
#
#     sql = ' select order_code from np_order a, np_customer b where a.customer_id = b.customer_id and ' \
#           'b.customer_username = "tengliang" order by order_code desc limit 1;'
#
#     mysqlope = MySqlOperator()
#     data = mysqlope.execute(sql)[0][0]
#
#     div = "div{}".format(str(data))
#     mysqlope.close()
#     div = 'div1808011147376053'
#     bo2.id_text_click(div, mobile.cancel_order)
#     sleep(1)
#     bo2.driver.find_element_by_class_name(mobile.css_confirm).click()
#
#     sleep(2)
#     bo2.close()
#     print i


def aa(a,b=None):
    # b=z
    if not b:
        b = 3
        print "b is {}".format(str(b))
    c=b+2
    print "c is {}".format(c)

aa('s')
