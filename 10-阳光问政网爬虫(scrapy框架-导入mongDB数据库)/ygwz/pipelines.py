# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from ygwz.items import YgwzItem
from pymongo import *

class YgwzPipeline(object):
    # 当爬虫启动时使用回调函数
    def open_spider(self, spider):
        #传到mongo中，需要先打开mongod
        client = MongoClient("127.0.0.1",port=27017)
        self.db= client.ygzw

    # 处理数据流
    def process_item(self, item, spider):

        # 因为item是scrapy.item的数据模型，需要线转化成python数据类型才能插入mongo
        #dict(item)转化为python的字典
        self.db.items.insert(dict(item))
        return item

    # 当爬虫结束时回调
    def close_spider(self, spider):
         pass