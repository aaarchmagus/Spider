# 利用生产消费模式，把url等都先放到queue中
import requests
# from queue import Queue
from lxml import etree
# import threading
# 多进程爬取糗事百科很简单，导入process和joinablequeue
from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue

class QiushiSpider(object):
    """ 这里写一个糗事百科的爬虫,利用生产消费模式"""
    def __init__(self):
        # 准备基础的数据base_url和headers
        self.base_url="https://www.qiushibaike.com/text/{}/"
        self.headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
        }
        # 准备三个队列，分别存放url list,获取的html数据，还有相关文字内容的数据
        self.url_Queue=Queue()
        self.html_Queue=Queue()
        self.item_Queue=Queue()


    def get_url_list(self):
        # 该方法主要是生产url的列表，放到url_queue中
        for n in range(1,14):
            self.url_Queue.put(self.base_url.format(n))
            # print(self.base_url)

    def parse_url(self):
        # 该方法主要用于解析url地址，并且发送请求获取html内容
        # 因为这个方法应该是一直跑的，不然取到一个url结束了。
        while True:
            url = self.url_Queue.get()
            response = requests.get(url=url, headers=self.headers)
            html = response.content.decode("utf-8")
            # print(html)
            self.html_Queue.put(html)
            # 注意，这里get urlqueue后要task_done，让unifinished task-1
            # 因为后面的代码都有queue.join挂起了主进程，如果不task_done，这些挂起的进程没办法关闭，会无限占用资源。
            self.url_Queue.task_done()

    def parse_item(self):
        #解析html，获取item数据,要一直解析，直到主进程被关闭
        while True:
            html = self.html_Queue.get()
            eroot = etree.HTML(html)
            texts = eroot.xpath('.//div[@class="content"]//span/text()')
            for item in texts:
                self.item_Queue.put(item)
            #同理要task_done
            self.html_Queue.task_done()

    def save_items(self):
        # 保存item
        while True:
            item = self.item_Queue.get()
            print(item)
            self.item_Queue.task_done()


    def run(self):
        tasks=[]
        get_url_list_task = Process(target=self.get_url_list)
        tasks.append(get_url_list_task)

        for i in range(5): # 这里为每个线程通过循环的方式开了5个线程，提高效率
            parse_url_task = Process(target=self.parse_url)
            tasks.append(parse_url_task)

        for i in range(3):
            parse_item_task = Process(target=self.parse_item)
            tasks.append(parse_item_task)

        for i in range(2):  #通常前面的要线程多一点，后面的保存方法线程要少，因为前面的处理考虑延迟，处理时间，开销大。
            save_item_task = Process(target=self.save_items)
            tasks.append(save_item_task)

        # 这里为什么要把开出来线程名放到列表tasks中，主要是为了写的时候省力，不然每个线程都要通过线程名.start开启
        for task in tasks:
            # 设置守护主线程，即主线程结束程序就关闭。
            # 这里有个问题，就是主线程如果强制结束，很有可能数据没取完
            # task.setDaemon(True)
            task.daemon = True
            task.start()

        # 所以为了让主线程不关闭，设置队列.join可以让主线程挂起
        # 只有通过task_done证明数据已经去玩了，主线程才会关闭
        self.url_Queue.join()
        self.html_Queue.join()
        self.item_Queue.join()


if __name__ == '__main__':
    qiushiSpider = QiushiSpider()
    qiushiSpider.run()