#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
分析 https://hr.tencent.com/position.php?lid=&tid=&keywords=&start={}
start 10 一页

爬虫思路：
获取第一页 拿到 总条数

计算总页数

循环获取列表页

提取数据

'''

import requests
from bs4 import BeautifulSoup
import math
import json

class TencentSpider(object):

    def __init__(self):
        self.base_url = "https://hr.tencent.com/position.php?lid=&tid=&keywords=&start={}"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }
        self.items = []
        pass

    def save_items(self):
        with open('06-data.json','w',encoding='utf-8') as f:
            json.dump(self.items,f,ensure_ascii=False,indent=2)

        pass

    def run(self):

        total_page_response = requests.get(self.base_url.format(0),headers = self.headers)
        total_page_html = total_page_response.text

        total_soup = BeautifulSoup(total_page_html,'lxml')

        total_count = total_soup.select(".lightblue.total")[0].get_text()

        # 通过总条数计算总页数
        # ceil 在很多编程语言里面都是表示 向上取整
        # floor 向下取整
        total_page = math.ceil(int(total_count) / 10.0)

        # 循环获取
        for start in range(0,total_page * 10,10):
            url = self.base_url.format(start)
            list_page_response = requests.get(url,headers = self.headers)
            list_page_html = list_page_response.text

            # 行数据解析
            list_page_soup = BeautifulSoup(list_page_html,'lxml')
            rows = list_page_soup.select('.even,.odd')
            for row in rows:
                item = {}

                item["name"] = row.select('a')[0].get_text()
                item["cate"] = row.select('td')[1].get_text()
                item["count"] = row.select('td')[2].get_text()
                item["location"] = row.select('td')[3].get_text()
                item["time"] = row.select('td')[4].get_text()

                self.items.append(item)

            break

        self.save_items()
        pass


if __name__ == '__main__':
    spider = TencentSpider()

    spider.run()