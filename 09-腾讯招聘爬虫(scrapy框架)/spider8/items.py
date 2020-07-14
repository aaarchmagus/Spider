# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
item.py这个模块里可以定义模型对象。
什么是模型对象？数据库的字段就是模型。
固定的写法是 字段名称 = scrapy.Field()

为什么要模型对象？
防止爬虫代码里字段错误导致数据白爬。

使用模型对象后，不再是python数据类型，所以需要dict（模型对象）转换成python数据


"""
class ItcastItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    desc = scrapy.Field()
    test = scrapy.Field()
    pass


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    cate = scrapy.Field()
    count = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()
    duty = scrapy.Field()
    require= scrapy.Field()
    pass


class Sun0769Item(scrapy.Item):
    # 阳光政务的item
    code = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    # duty = scrapy.Field()
    # require= scrapy.Field()
    pass