import scrapy
from ygwz.items import YgwzItem
from scrapy.http.request import Request

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    base_url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page={}'

    def start_requests(self):

        for start in range(0, 100920, 30):
            url = self.base_url.format(start)
            req = Request(
                url=url,
                # 如果不填写callback系统会自动调用parse
                callback=self.parse_list
            )
            yield req
            break # 这里break是为了调试，就一个url就break

    def parse_list(self, response):
        # 这里因为阳光政务的网页结构问题，反推xpath更加简单
        tr_list = response.xpath('//a[@class="news14"]/../..')

        for tr in tr_list:
            item = YgwzItem()
            item["num_id"] = tr.xpath('.//td[1]/text()').extract_first()
            item["title"] = tr.xpath('.//td[2]//a[@class="news14"]/text()').extract_first()
            item["status"] = tr.xpath('.//td[3]//text()').extract_first()
            item["author"] = tr.xpath('.//td[4]/text()').extract_first()
            item["time"] = tr.xpath('.//td[5]//text()').extract_first()
            print(item)

            # 获取详情页
            href = tr.xpath('.//td[2]//a[@class="news14"]/@href').extract_first()
            if href is not None:
                detail_url = href
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


    def parse_detail(self,response):

        #从响应中提取meta数据
        item = response.meta["item"]
        print(item)

        item["content"] = response.xpath('//td[@class="txt16_3"]//text()').extract_first()


        # 因为之前的响应已经提取了meta数据item ，这里组装duty和require字段后就可以提交了
        yield item
