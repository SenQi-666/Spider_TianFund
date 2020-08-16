from spider_tianFund.items import SpiderTotalFundItem, SpiderFundInfoItem
from urllib.parse import urlencode
import scrapy
import json
import math
import re


class FundSpider(scrapy.Spider):
    name = 'Fund'
    allowed_domains = ['fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/js/fundcode_search.js']
    detail_url = 'http://api.fund.eastmoney.com/f10/lsjz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            headers=self.headers,
            callback=self.parse,
        )

    def parse(self, response):
        item = SpiderTotalFundItem()
        fund_json = re.findall('var r = (.*?);', response.text)[0]
        fund_lst = json.loads(fund_json)
        for fund_detail in fund_lst:
            item['FundCode'] = fund_detail[0]
            item['FundName'] = fund_detail[2]
            item['FundType'] = fund_detail[3]
            yield item

            origin_url = 'http://fundf10.eastmoney.com/jjjz_%s.html' % fund_detail[0]
            self.headers['Referer'] = origin_url
            params = {
                'fundCode': fund_detail[0],
                'pageIndex': 9999999,
                'pageSize': 20,
            }
            url = self.detail_url + '?' + urlencode(params)
            yield scrapy.Request(url, headers=self.headers, callback=self.get_total_count,
                                 meta={'item': item})

    def get_total_count(self, response):
        print(response.json())
        count = response.json()['TotalCount']
        fund_code = response.meta['item']['FundCode']
        total_page = math.ceil(count / 20)
        print(fund_code, count, total_page)
        page_index = 1
        while page_index <= total_page:
            params = {
                'fundCode': fund_code,
                'pageIndex': page_index,
                'pageSize': 20,
            }
            url = self.detail_url + '?' + urlencode(params)
            yield scrapy.Request(url, headers=self.headers, callback=self.get_info,
                                 meta={'item': response.meta['item']})
            page_index += 1

    def get_info(self, response):
        item = SpiderFundInfoItem()
        item['FundCode'] = response.meta['item']['FundCode']
        item['FundName'] = response.meta['item']['FundName']
        data = response.json()['Data']
        if data:
            date_lst = []
            unit_value = []
            total_value = []
            growth_rate = []
            purch_status = []
            ransom_status = []
            for fund_item in data['LSJZList']:
                date_lst.append(fund_item['FSRQ'])
                unit_value.append(fund_item['DWJZ'])
                total_value.append(fund_item['LJJZ'])
                growth_rate.append(fund_item['JZZZL'])
                purch_status.append(fund_item['SGZT'])
                ransom_status.append(fund_item['SHZT'])
            item['Date'] = date_lst
            item['UnitValue'] = unit_value
            item['TotalValue'] = total_value
            item['GrowthRate'] = growth_rate
            item['PurchStatus'] = purch_status
            item['RansomStatus'] = ransom_status
            yield item
