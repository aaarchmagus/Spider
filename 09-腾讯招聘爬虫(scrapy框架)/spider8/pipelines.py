# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from spider8.items import ItcastItem
from spider8.items import TencentItem

# 两个管道的执行顺序是由settings.py中ITEM_PIPELINES配置值决定的，数字越小越优先
# 301比300晚执行
# 管道类的process_item函数必须有返回值return item，不然后面一个管道接收到的数据为NONE

class ItcastPipeline(object):
    # 一旦开启管道，process_item 会自动被scrapy引擎调用
    # item 就是引擎传递接收数据对象
    # spider item 来自哪个爬虫对象
    def process_item(self, item, spider):
        # 这里item过来有可能是tecent模型也可能是itcast，所以加入一个判断item是否属于itcastItem
        # 如果不是的话，直接返回，不对数据进行任何操作
        if not isinstance(item, ItcastItem):
            return item

        item["test"] = 1
        return item


class ItcastJsonPipeline(object):
    # 当爬虫启动时使用回调函数
    def open_spider(self, spider):
        self.f = open('new_data.json', "w", encoding='utf-8')
        self.f.write("[")

    # 处理数据流
    def process_item(self, item, spider):
        # 这里item过来有可能是tecent模型也可能是itcast，所以加入一个判断item是否属于itcastItem
        # 如果不是的话，直接返回，不对数据进行任何操作
        if not isinstance(item, ItcastItem):
            return item

        json.dump(dict(item), self.f, ensure_ascii=False, indent=2)
        self.f.write(",")
        return item

    # 当爬虫结束时回调
    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()

class TencentJsonPipeline(object):
    # 当爬虫启动时使用回调函数
    def open_spider(self, spider):
        self.f = open('tencent_data.json', "w", encoding='utf-8')
        self.f.write("[")

    # 处理数据流
    def process_item(self, item, spider):
        # 这里item过来有可能是tecent模型也可能是itcast，所以加入一个判断item是否属于itcastItem
        # 如果不是的话，直接返回，不对数据进行任何操作
        if not isinstance(item, TencentItem):
            return item
        json.dump(dict(item), self.f, ensure_ascii=False, indent=2)
        self.f.write(",")
        return item

    # 当爬虫结束时回调
    def close_spider(self, spider):
        self.f.write("]")
        self.f.close()