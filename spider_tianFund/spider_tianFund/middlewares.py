# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import requests
import random
import time
from lxml import etree


class MyUserAgent:
    ua_lst = []

    def __init__(self):
        self.url = 'https://lc-0owj6syh.cn-e1.lcfile.com/0f8f9ab623d0d0f1e109/UA_Pool.html'
        self.get()

    def get(self):
        response = requests.get(self.url)
        html = etree.HTML(response.text)
        self.ua_lst = html.xpath('//p/text()')


class MyProxies:
    ip_lst = []

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.get()

    def get(self):
        for num in range(1, 6):
            url = 'https://www.kuaidaili.com/free/inha/%d/' % num
            response = requests.get(url, headers=self.headers, timeout=5)
            html = etree.HTML(response.text)
            ips = html.xpath('//*[@id="list"]/table//tr/td[1]/text()')
            ports = html.xpath('//*[@id="list"]/table//tr/td[2]/text()')
            [self.ip_lst.append('http://%s:%s' % (ip, port)) for ip, port in zip(ips, ports)]
            time.sleep(1)


UA_LST = MyUserAgent().ua_lst
PROXIES = MyProxies().ip_lst


class SpiderFundDownloaderMiddleware:
    def __init__(self):
        self.user_agent = random.choice(UA_LST)
        self.proxy = random.choice(PROXIES)

    def process_request(self, request, spider):
        print('Replace the UA and the Proxy')
        request.headers['User-Agent'] = self.user_agent
        print(request.headers)
        request.meta['proxy'] = self.proxy
        print(request.meta)

    def process_exception(self, request, exception, spider):
        print('Get the data exception, replace the UA and the Proxy again')
        self.process_request(request, spider)
