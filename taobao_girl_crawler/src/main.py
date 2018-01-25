# -*- coding:utf-8 -*-
from src.writer.Writer import *
# 全局变量
page_num = 10
if __name__ == '__main__':
    for page in range(page_num):
        writeInfo(page)