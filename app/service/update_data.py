"""读取 csv 测试文件内容, 存储到数据库"""
import pandas as pd

from app.common.utils import time_it
from app.models.set.FundDescription import FundDescription
from app.models.set.FundNav import FundNav
from configs.db_config import db


class CacheData(object):
    @classmethod
    @time_it
    def update_desc_data(cls):
        file_path = '/Users/zxl/sx/flaskProject/fund_description.csv'
        sheet = pd.read_csv(file_path, encoding='utf-8', converters={'fund_id': str})
        fund_ids = sheet.iloc[:, 0].fillna('')
        fund_names = sheet.iloc[:, 1].fillna('')

        objects = []
        for f_id, f_name in zip(fund_ids, fund_names):
            objects.append(FundDescription(fund_id=f_id, fund_name=f_name))

        db.session.add_all(objects)
        db.session.commit()

    @classmethod
    @time_it
    def update_nv_data(cls):
        file_path = '/Users/zxl/sx/flaskProject/fund_nav.csv'
        sheet = pd.read_csv(file_path, encoding='utf-8', converters={'fund_id': str})
        fund_ids = sheet.iloc[:, 0].fillna('')
        trade_dates = sheet.iloc[:, 1].fillna('')
        nav_units = sheet.iloc[:, 2].fillna('')

        for f_id, trade_date, nav_unit in zip(fund_ids, trade_dates, nav_units):
            FundNav.add(**dict(fund_id=f_id, trade_date=trade_date, nav_unit=nav_unit))





