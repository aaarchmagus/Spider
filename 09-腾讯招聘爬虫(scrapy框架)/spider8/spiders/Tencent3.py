# -*- coding: utf-8 -*-
import scrapy
from spider8.items import TencentItem
from scrapy.http.request import Request

class TecentSpider(scrapy.Spider):
    name = 'Tencent3'
    allowed_domains = ['tencent.com']

    # 利用并发
    base_url = 'https://hr.tencent.com/position.php?keywords=&lid=0&start={}'
    # start_urls = []
    # for start in range (0,2800,10):
    #     start_urls.append((base_url.format(start)))


    # 上面这样写urls虽然实现了并发，但是只能请求url地址，通常来说requests还包含更多的东西
    # 如何定制自己的request，除了url，可能headers，cookie都不一样
    #  scrapy引擎包含start_requests方法，写了这个方法引擎会自动调用并开始获取请求对象，start_urls就不再起作用。

    def start_requests(self):

        # 1. 第一种写法，通过返回请求列表
        # reqs = []
        # for start in range(0, 2800, 10):
        #     url = self.base_url.format(start)
        #     req = Request(
        #         url=url,
        #         # 如果不填写callback系统会自动调用parse
        #         callback = self.parse
        #     )
        #     reqs.append(req)
        #
        # return reqs

        # 1. 第二种写法，通过yield请求列表，不需要reqs列表了
        for start in range(0, 2800, 10):
            url = self.base_url.format(start)
            req = Request(
                url=url,
                # 如果不填写callback系统会自动调用parse
                callback=self.parse
            )
            yield req




    def parse(self, response):
        tr_list = response.css('.even,.odd')

        for tr in tr_list:
            item = TencentItem()
            item["name"] = tr.xpath('.//a/text()').extract_first()
            item["cate"] = tr.xpath('./td[2]/text()').extract_first()
            item["count"] = tr.xpath('./td[3]/text()').extract_first()
            item["location"] = tr.xpath('./td[4]/text()').extract_first()
            item["time"] = tr.xpath('./td[5]/text()').extract_first()
            # print(item)

            yield item


