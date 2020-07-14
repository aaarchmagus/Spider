# -*- coding: utf-8 -*-
import scrapy
from spider8.items import TencentItem
from scrapy.http.request import Request

class TecentSpider(scrapy.Spider):
    name = 'Tencent4'
    allowed_domains = ['tencent.com']
    base_url = 'https://hr.tencent.com/position.php?keywords=&lid=0&start={}'

    def start_requests(self):

        for start in range(0, 2800, 10):
            url = self.base_url.format(start)
            req = Request(
                url=url,
                # 如果不填写callback系统会自动调用parse
                callback=self.parse_list
            )
            yield req
            break # 这里break是为了调试，就一个url就break

    def parse_list(self, response):

        tr_list = response.css('.even,.odd')

        for tr in tr_list:
            item = TencentItem()
            item["name"] = tr.xpath('.//a/text()').extract_first()
            item["cate"] = tr.xpath('./td[2]/text()').extract_first()
            item["count"] = tr.xpath('./td[3]/text()').extract_first()
            item["location"] = tr.xpath('./td[4]/text()').extract_first()
            item["time"] = tr.xpath('./td[5]/text()').extract_first()
            # print(item)
            # yield item

            # 获取详情页
            href = tr.xpath('.//a/@href').extract_first()
            if href is not None:
                detail_url = "https://hr.tencent.com/"+href
                # 发送请求给引擎获取响应
                req = Request (
                    url = detail_url,
                    callback=self.parse_detail,
                    # 之前item的数据没有yield，这里要利用meta进行传递
                    meta = {
                        "item":item
                    }
                )
                yield req

            break  #为了调试，就获取一个请求
    def parse_detail(self,response):

        #从响应中提取meta数据
        item = response.meta["item"]
        print(item)

        uls = response.xpath('//ul[@class="squareli"]')
        item["duty"] = "\n".join(uls[0].xpath("./li/text()").extract())
        item["require"] = "\n".join(uls[1].xpath("./li/text()").extract())

        # 因为之前的响应已经提取了meta数据item，这里组装duty和require字段后就可以提交了
        yield item


