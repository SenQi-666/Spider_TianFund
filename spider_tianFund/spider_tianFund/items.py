# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderTotalFundItem(scrapy.Item):
    FundCode = scrapy.Field()    # 基金代码
    FundName = scrapy.Field()    # 基金名称
    FundType = scrapy.Field()    # 基金类型


class SpiderFundInfoItem(scrapy.Item):
    FundCode = scrapy.Field()    # 基金代码
    FundName = scrapy.Field()    # 基金名称
    Date = scrapy.Field()    # 净值日期
    UnitValue = scrapy.Field()    # 单位净值
    TotalValue = scrapy.Field()    # 累计净值
    GrowthRate = scrapy.Field()    # 日增长率
    PurchStatus = scrapy.Field()    # 申购状态
    RansomStatus = scrapy.Field()    # 赎回状态
