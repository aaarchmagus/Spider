# -*- coding: utf-8 -*-
import scrapy
from spider8.items import TencentItem
from scrapy.http.request import Request

class TecentSpider(scrapy.Spider):
    name = 'Tencent'
    allowed_domains = ['tencent.com']
    # start_urls = ['https://hr.tencent.com/position.php?lid=&tid=&keywords=']
    # 用页数少的界面测试翻页是否成功
    start_urls = ['https://hr.tencent.com/position.php?keywords=&lid=2196&tid=82']

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

        next_url=response.xpath('//a[@id="next"]/@href').extract_first()
        print("next_url")
        # 这里需要判断next_url是否为none就是没有下一页了，还有一种情况最后一页的数据是'javascipt:;'
        if next_url is not None and next_url != 'javascript:;':
            next_url = "https://hr.tencent.com/" + next_url

            # 继续发送请求
            # 1. 构建请求对象（需要导入scrapy的requests对象）,然后就是callback回调parse解析函数
            req = Request(
                url=next_url,
                callback=self.parse
            )

            # 2. 把请求交给引擎
            yield req

