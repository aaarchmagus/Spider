# -*- coding: utf-8 -*-
import scrapy
from spider8.items import ItcastItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # print(response.body.decode("utf-8"))
        # print(response.xpath('//div[@class ="li_txt"]/h3/text()').extract())

        # response.xpath ---> 其实是selector对象的xpath方法
        # selector.xpath 返回的是列表对象，里面放置了selector对象
        # selector.css 也返回列表对象，这里css代表css选择器，里面也放置了selector对象
        div_list = response.xpath("""//div[@class ="li_txt"]""")
        for div in div_list:
            item = ItcastItem()
            #selector.xpath也就是response.xpath返回的是一个对象(不是一个单纯的列表）
            # 因此需要使用extract()把对象中的数据提取成列表
            # 如果需要提取该列表中的第一个数据，可以用name=div.xpath('./h5/text()')[0].extract()
            # 提取该列表的第一个数据还可以用extract_first()
            # 推荐使用extract_first()，因为查不到会返回None，而另一种方式会报错
            item["name"] = div.xpath('./h3/text()').extract_first()
            item["type"] = div.xpath('./h4/text()').extract_first()
            item["desc"] = div.xpath('./p/text()').extract_first()
            # print(item)

            yield item



        pass