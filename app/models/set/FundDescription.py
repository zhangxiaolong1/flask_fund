# -*- coding: UTF-8 -*-
from app.common.utils import SXCache
from configs.db_config import db
from app.models.base.base_model import BaseModel


class FundDescription(db.Model, BaseModel):
    __tablename__ = "fund_description"
    fund_id = db.Column(db.VARCHAR, primary_key=True)
    fund_name = db.Column(db.VARCHAR)

    def to_msg(self):
        return {
            "fund_id": self.fund_id,
            "fund_name": self.fund_name,
        }

    @classmethod
    def add(cls, **kwargs):
        try:
            _res = cls.create(**kwargs)
            return _res.to_dict()
        except Exception as e:
            print('create new row fail')
            print(e, e.args)


@SXCache(exp_time=3600)
def get_fund_desc_map():
    """根据 fund_id 获取对应的 {fund_id: fund_desc}"""
    funds = FundDescription.query.all()
    return {f.fund_id: f.to_msg() for f in funds}


def get_fund_desc(fund_id):
    """根据基金id或基金描述信息"""
    fund_map = get_fund_desc_map()
    fund_desc = fund_map.get(fund_id, {'fund_id': fund_id, 'fund_name': ''})
    return fund_desc


