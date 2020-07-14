# 利用生产消费模式，把url等都先放到queue中
# from multiprocessing.dummy import Pool
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
import requests
from queue import Queue
from lxml import etree



class QiushiSpider(object):
    """ 这里写一个糗事百科的爬虫,利用生产消费模式"""
    def __init__(self):
        # 准备基础的数据base_url和headers
        self.base_url="https://www.qiushibaike.com/text/{}/"
        self.headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
        }
        # 存放url list的queue
        self.url_Queue=Queue()
        # 初始化pool
        self.pool = Pool(5)

    def get_url_list(self):
        # 该方法主要是生产url的列表，放到url_queue中
        for n in range(1,14):
            self.url_Queue.put(self.base_url.format(n))
            # print(self.base_url)

    def exec_task(self):
        # 1.获取url地址
        url = self.url_Queue.get()
        # 2. 请求网页获取响应
        response = requests.get(url=url, headers=self.headers)
        html = response.content.decode("utf-8")
        # 3.解析数据
        eroot = etree.HTML(html)
        texts = eroot.xpath('.//div[@class="content"]//span/text()')
        for item in texts:
            # 4. 保存数据
            print(item)
        self.url_Queue.task_done()

    # 注意callback函数一定要带上ret返回值参数，否则会报错. 前序函数没有返回值其实是返回了none
    def exec_task_finished(self,ret):
        self.pool.apply_async(self.exec_task, callback=self.exec_task_finished)


    def run(self):
        # 首先获取url地址列表
        self.get_url_list()
        # 执行线程池代码
        for i in range(5):
            self.pool.apply_async(self.exec_task,callback=self.exec_task_finished)

        self.url_Queue.join()


if __name__ == '__main__':
    qiushiSpider = QiushiSpider()
    qiushiSpider.run()