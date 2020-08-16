# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pandas as pd
import os


class SpiderToCsvPipeline:
    BASE_DIR = os.path.join(os.path.dirname(__file__), 'spiders/Fund_Detail_Info')
    fund_type_dir = None

    def __init__(self):
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)

    def process_item(self, item, spider):
        if item.__class__.__name__ == 'SpiderTotalFundItem':
            self.fund_type_dir = os.path.join(self.BASE_DIR, item['FundType'])
            if not os.path.exists(self.fund_type_dir):
                os.mkdir(self.fund_type_dir)
                print(f'创建 {self.fund_type_dir} 目录成功')
        else:
            csv_name = f"{item.pop('FundCode')}_{item.pop('FundName')}.csv"
            csv_path = os.path.join(self.fund_type_dir, csv_name)
            dataframe = pd.DataFrame({
                '净值日期': item['Date'],
                '单位净值': item['UnitValue'],
                '累计净值': item['TotalValue'],
                '日增长率': item['GrowthRate'],
                '申购状态': item['PurchStatus'],
                '赎回状态': item['RansomStatus']
            })
            if os.path.exists(csv_path):
                dataframe.to_csv(csv_path, mode='a', index=False, header=False, sep=',', encoding="ANSI")
            else:
                dataframe.to_csv(csv_path, index=False, sep=',', encoding="ANSI")
