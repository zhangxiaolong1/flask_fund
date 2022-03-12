# -*- coding: UTF-8 -*-
import datetime

from sqlalchemy import desc, func

from app.common.constants import DATE_FORMAT
from app.common.utils import time_it, format_float, SXCache
from configs.db_config import db
from app.models.base.base_model import BaseModel


class FundNav(db.Model, BaseModel):
    __tablename__ = "fund_nav"
    id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.VARCHAR)
    trade_date = db.Column(db.DateTime)
    nav_unit = db.Column(db.Float)

    def to_msg(self):
        return {
            "fund_id": self.fund_id,
            "trade_date": self.trade_date,
            "nav_unit": self.nav_unit
        }

    @classmethod
    def add(cls, **kwargs):
        try:
            _res = cls.create(**kwargs)
            return _res.to_dict()
        except Exception as e:
            print('create new row fail')
            print(e, e.args)


@time_it
@SXCache(exp_time=3600)
def get_fund_index_info(fund_id):
    """根据 fund_id 获取对应的日涨跌幅， 年涨跌幅"""

    now_fund = FundNav.query.filter_by(fund_id=fund_id).order_by(desc(FundNav.trade_date)).first()
    if not now_fund:
        raise Exception("该基金不存在，请检查输入的 fund_id")
    trade_date = now_fund.trade_date
    day_trade_date = (trade_date + datetime.timedelta(days=-1)).strftime(DATE_FORMAT)
    year_trade_date = (trade_date + datetime.timedelta(days=-365)).strftime(DATE_FORMAT)
    day_fund = get_fund_nav_by_id_trade(fund_id, day_trade_date)
    year_fund = get_fund_nav_by_id_trade(fund_id, year_trade_date)
    day_index = (now_fund.nav_unit - day_fund.get('nav_unit', 0))/day_fund.get('nav_unit', 0) if day_fund.get('nav_unit', 0) else 0
    year_index = (now_fund.nav_unit - year_fund.get('nav_unit', 0))/year_fund.get('nav_unit', 0) if year_fund.get('nav_unit', 0) else 0

    res = now_fund.to_msg()
    res.update(dict(day_index=format_float(day_index), year_index=format_float(year_index)))

    return res


def get_fund_nav_by_id_trade(fund_id, trade):
    """根据fund_id trade 获取对应的数据"""
    fund = FundNav.query.filter(FundNav.fund_id == fund_id, FundNav.trade_date == trade).first()
    if fund:
        return fund.to_msg()
    else:
        return {}


def get_fund_nav_list(page_id, page_size):
    """根据 查询fund_id 获取对应的数据"""
    last_fund_navs = get_last_nav()
    res = FundNav.query.filter(FundNav.fund_id == last_fund_navs.c.fund_id, FundNav.trade_date == last_fund_navs.c.trade_date).order_by(last_fund_navs.c.trade_date.desc()).paginate(
            int(page_id),
            per_page=int(page_size),
            error_out=False
        ).items
    return res


@SXCache(exp_time=3600)
def get_last_nav():
    """获取最近的交易时间"""
    last_fund_navs = FundNav.query.with_entities(FundNav.fund_id, func.max(FundNav.trade_date).label('trade_date')).group_by(FundNav.fund_id).subquery()
    return last_fund_navs


@SXCache(exp_time=3600)
def get_fun_nav_interval_trend(fund_id, interval):
    """获取 fund_id 的 最近 interval 的数据"""
    last_fund_nav = FundNav.query.with_entities(FundNav.fund_id, func.max(FundNav.trade_date).label('trade_date')).filter_by(fund_id=fund_id).first()
    start_date = (last_fund_nav.trade_date + datetime.timedelta(days=-interval)).strftime(DATE_FORMAT)

    fund_navs = FundNav.query.filter(FundNav.fund_id == fund_id, FundNav.trade_date >= start_date).order_by(FundNav.trade_date.desc()).all()

    return fund_navs



