# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from time import sleep


def wait_for_display(path_type):
    if path_type == 'xpath':
        by = By.XPATH
    elif path_type == 'text':
        by = By.LINK_TEXT
    elif path_type == 'p_text':
        by = By.PARTIAL_LINK_TEXT
    elif path_type == 'id':
        by = By.ID

    def outer(func):
        def wait_until(self, path, *args, **kwargs):
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, path)))
                # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, path)))
            except Exception:
                print "cannot find the element "

            func(self, path, *args, **kwargs)
        return wait_until
    return outer


def check_timeout(func):
    # 如果页面超时则停止页面，继续后面操作
    def check(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except TimeoutException:
            self.driver.execute_script('window.stop()')

    return check


class BrowserOperator(object):

    def __init__(self, logger, name=None):

        # 使用firefox驱动
        self.driver = webdriver.Firefox()
        # 使用chrome驱动
        # self.driver = webdriver.Chrome()
        # 使用chrome headless(无图形界面)驱动
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.logger = logger
        self.name = name
        self.driver.implicitly_wait(2)
        self.driver.set_page_load_timeout(10)
        self.driver.set_window_size(480, 1000)

    @check_timeout
    def get_url(self, url):
        self.driver.get(url)

    @check_timeout
    def id_input(self, eid, value):
        self.driver.find_element_by_id(eid).send_keys(value)

    @check_timeout
    def id_click(self, eid):
        self.driver.find_element_by_id(eid).click()

    @check_timeout
    def id_clean(self, eid):
        sleep(1)
        self.driver.find_element_by_id(eid).clear()

    def id_text(self, eid):
        sleep(1)
        return self.driver.find_element_by_id(eid).text

    @check_timeout
    def id_css_click(self, eid, css):
        sleep(1)
        self.driver.find_element_by_id(eid).find_element_by_class_name(css).click()

    @check_timeout
    def id_text_click(self, eid, text):
        sleep(1)
        self.driver.find_element_by_id(eid).find_element_by_link_text(text).click()

    @check_timeout
    def id_css_click(self, eid, css):
        sleep(1)
        self.driver.find_element_by_id(eid).find_element_by_class_name(css).click()

    @check_timeout
    def xpath_fill_input(self, xpath, value):
        sleep(1)
        self.driver.find_element_by_xpath(xpath).send_keys(value)

    @check_timeout
    def xpath_click(self, xpath):
        sleep(1)
        self.driver.find_element_by_xpath(xpath).click()

    @check_timeout
    def xpath_send_enter(self, xpath):
        sleep(1)
        self.driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)

    @check_timeout
    def text_click(self, text):
        # find element by link text
        sleep(1)
        self.driver.find_element_by_link_text(text).click()

    @check_timeout
    def p_text_click(self, text):
        # find element by partial link text
        sleep(1)
        self.driver.find_element_by_partial_link_text(text).click()

    @check_timeout
    def class_click(self, css):
        sleep(1)
        self.driver.find_element_by_class_name(css).click()

    @check_timeout
    def go_back(self):
        sleep(1)
        self.driver.back()

    def exec_script(self, script):
        self.driver.execute_script(script)

    def close(self):
        self.driver.close()


