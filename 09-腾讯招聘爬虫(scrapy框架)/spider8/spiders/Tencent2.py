# -*- coding: utf-8 -*-
import scrapy
from spider8.items import TencentItem
from scrapy.http.request import Request

class TecentSpider(scrapy.Spider):
    name = 'Tencent2'
    allowed_domains = ['tencent.com']

    # 利用并发
    base_url = 'https://hr.tencent.com/position.php?keywords=&lid=0&start={}'
    start_urls = []
    for start in range (0,2800,10):
        start_urls.append((base_url.format(start)))

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


