#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2017/9/8
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#等待网页相应
from selenium.webdriver.support.ui import WebDriverWait as WDW
#负责条件
from selenium.webdriver.support import expected_conditions as EC
#超时
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
#打开浏览器
# driver = webdriver.PhantomJS(executable_path='D:/zhuliquan/Documents/WorkSpace/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver = webdriver.Chrome()
#打开网页
driver.get("https://www.taobao.com")
#延时等待的对象
wait = WDW(driver,40)

def get_info(goods):
    # 锁定输入框
    try:
        # 等待输入框加载
        input = wait.until(
            # 条件是元素可以被定为
            EC.presence_of_element_located(
                # 定位的方法
                (By.CSS_SELECTOR, "#q")
            )
        )
        input.send_keys(goods)
        # 等待按钮加载
        button = wait.until(
            # 条件是元素可以点击
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")
            )
        )
        button.click()
        # 翻10页的网页
        for _ in range(0, 1):
            get_response()
            time.sleep(5)
            next_page()
    except Exception as e:
        print("出现错误")
    finally:
        driver.close()
def get_response():
    html_page = driver.page_source
    soup = BeautifulSoup(html_page,'html.parser')
    items = soup.find("div",attrs={"id":"mainsrp-itemlist"}).find("div").find("div").find("div").find_all("div")
    for item in items:
        product = {
            "img_src" : item.find("img", attrs={"class": "J_ItemPic img"})["src"],
            "img_alt" : item.find("img", attrs={"class": "J_ItemPic img"})["alt"],
            # "price"   : item.find("div", attrs={"class": "price g_price g_price-highlight"}).find("strong").string,
            # "cnt"     : item.find("div", attrs={"class": "deal-cnt"}).string,
        }
        print(product)


def next_page():
    page_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.next > a")
        )
    )
    page_button.click()

if __name__ == "__main__":
    get_info("python")