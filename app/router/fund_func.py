from flask import request
from flask_restplus import Namespace, Resource

from app.common.utils import sx_json
from app.models.set.FundDescription import get_fund_desc
from app.models.set.FundNav import get_fund_index_info, get_fund_nav_list, get_fun_nav_interval_trend
from app.service.update_data import CacheData

fund_func = Namespace("fund_func", description="基金功能接口")


@fund_func.route("/detail")
class Detail(Resource):
    @fund_func.param("fund_id", "基金id")
    def get(self):
        """

        基金详情

        * 返回格式：Json

        * 备注：返回一个基金的详情

        * 请求参数说明：

            | 名称 | 类型 | 必填 |说明|
            |----- |------| ---- |----|
            |fund_id |string|true|基金 id|
        * 请求实例：
            - fund_id: 002654

        * 返回参数说明：

            | 名称 | 类型 |说明|
            |----- |------|----|
            | code | int|状态码
            |data | object|具体数据|
            |day_index | string|最新日涨跌幅|
            |fund_id | string|基金 id|
            |fund_name | string|基金简称|
            |nav_unit | float|最新单位净值|
            |trade_date | datetime|最新交易日期|
            |year_index | string|近一年涨跌幅|
            |extra_data | object|其他数据|
            |msg | string|请求状态信息|

        * JSON返回示例：

             {
                  "code": 200,
                  "data": {
                    "day_index": "-0.03%",
                    "fund_id": "002654",
                    "fund_name": "上投摩根策略精选",
                    "nav_unit": 1.5257,
                    "trade_date": "Wed, 03 Nov 2021 00:00:00 GMT",
                    "year_index": "9.83%"
                  },
                  "extra_data": null,
                  "msg": "success"
            }

        ---
        """
        data = request.args
        fund_id = data.get('fund_id')
        res = get_fund_detail(fund_id)

        return sx_json(200, res)


@fund_func.route("/list")
class FundList(Resource):
    @fund_func.param("page_id", "页码", type=int)
    @fund_func.param("page_size", "页量", type=int)
    def get(self):
        """

        基金列表

        * 返回格式：Json

        * 备注：返回基金的列表

        * 请求参数说明：

            | 名称 | 类型 | 必填 |说明|
            |----- |------| ---- |----|
            |page_id |integer|true|页码|
            |page_size |integer|true|页量|

        * 请求实例：

            - page_id: 1
            - page_size: 3

        * 返回参数说明：

            | 名称 | 类型 |说明|
            |----- |------|----|
            | code | int|状态码
            |data | object|具体数据|
            |day_index | string|最新日涨跌幅|
            |fund_id | string|基金 id|
            |fund_name | string|基金简称|
            |nav_unit | float|最新单位净值|
            |trade_date | datetime|最新交易日期|
            |year_index | string|近一年涨跌幅|
            |extra_data | object|其他数据|
            |msg | string|请求状态信息|

        * JSON返回示例：

             {
              "code": 200,
              "data": [
                {
                  "day_index": "-2.56%",
                  "fund_id": "110011",
                  "fund_name": "易方达优质精选",
                  "nav_unit": 6.3155,
                  "trade_date": "Fri, 04 Mar 2022 00:00:00 GMT",
                  "year_index": "-21.38%"
                },
                {
                  "day_index": "-0.66%",
                  "fund_id": "162605",
                  "fund_name": "景顺鼎益LOF",
                  "nav_unit": 2.559,
                  "trade_date": "Fri, 04 Mar 2022 00:00:00 GMT",
                  "year_index": "-17.69%"
                },
                {
                  "day_index": "-1.59%",
                  "fund_id": "004812",
                  "fund_name": "中欧先进制造A",
                  "nav_unit": 3.1553,
                  "trade_date": "Fri, 04 Mar 2022 00:00:00 GMT",
                  "year_index": "27.23%"
                }
              ],
              "extra_data": null,
              "msg": "success"
            }


        ---
        """

        data = request.args
        page_id, page_size = data.get('page_id', 0, type=int), data.get('page_size', 3, type=int)
        res = get_fund_list(page_id, page_size)
        return sx_json(200, res)


@fund_func.route("/income_trend")
class IncomeTrend(Resource):
    @fund_func.param("fund_id", "基金id")
    @fund_func.param("interval", "间隔天数", type=int)
    def get(self):
        """
        业绩走势

        * 返回格式：Json

        * 备注：返回一个基金的不同时间段内累计收益率的时间序列

        * 请求参数说明：

            | 名称 | 类型 | 必填 |说明|
            |----- |------| ---- |----|
            |fund_id |string|true|基金 id|
            |interval |integer|true|间隔天数|
        * 请求实例：
            - fund_id: 513050
            - interval: 30

        * 返回参数说明：

            | 名称 | 类型 |说明|
            |----- |------|----|
            | code | int|状态码
            |data | object|具体数据|
            |income_rate | string|累计收益率|
            |trade_date | datetime|最新交易日期|
            |extra_data | object|其他数据|
            |msg | string|请求状态信息|

        * JSON返回示例：

             {
              "code": 200,
              "data": [
                {
                  "income_rate": -0.13222531521205172,
                  "trade_date": "Thu, 03 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.10463402652693643,
                  "trade_date": "Wed, 02 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.09685606680858039,
                  "trade_date": "Tue, 01 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.10749959063369896,
                  "trade_date": "Mon, 28 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.0966104470280007,
                  "trade_date": "Fri, 25 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.09726543310954638,
                  "trade_date": "Thu, 24 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.07810709022433282,
                  "trade_date": "Wed, 23 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.0704928770263632,
                  "trade_date": "Tue, 22 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.04519403962665802,
                  "trade_date": "Mon, 21 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.022105780252169804,
                  "trade_date": "Fri, 18 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.027100049123956138,
                  "trade_date": "Thu, 17 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.029556246929752783,
                  "trade_date": "Wed, 16 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.024480104797773183,
                  "trade_date": "Tue, 15 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.01326346815130175,
                  "trade_date": "Mon, 14 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.02611757000163739,
                  "trade_date": "Fri, 11 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.046913378090715385,
                  "trade_date": "Thu, 10 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.05084329457999015,
                  "trade_date": "Wed, 09 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.014000327493040698,
                  "trade_date": "Tue, 08 Feb 2022 00:00:00 GMT"
                }
              ],
              "extra_data": null,
              "msg": "success"
            }

        ---
        """
        data = request.args
        fund_id, interval = data.get('fund_id'), data.get('interval', 30, type=int)
        res, count = get_fund_income_rate_trend(fund_id, interval)
        return sx_json(200, res)


@fund_func.route("/dynamic_trend")
class DynamicTrend(Resource):
    @fund_func.param("fund_id", "基金id")
    @fund_func.param("interval", "间隔天数", type=int)
    def get(self):
        """
        动态回撤曲线

        * 返回格式：Json

        * 备注：返回一个基金的不同时间段内动态回撤时间序列

        * 请求参数说明：

            | 名称 | 类型 | 必填 |说明|
            |----- |------| ---- |----|
            |fund_id |string|true|基金 id|
            |interval |integer|true|间隔天数|
        * 请求实例：
            - fund_id: 513050
            - interval: 30

        * 返回参数说明：

            | 名称 | 类型 |说明|
            |----- |------|----|
            | code | int|状态码
            |data | object|具体数据|
            |income_rate | string|累计收益率|
            |trade_date | datetime|最新交易日期|
            |extra_data | object|其他数据|
            |msg | string|请求状态信息|

        * JSON返回示例：

             {
              "code": 200,
              "data": [
                {
                  "income_rate": -0.13222531521205172,
                  "trade_date": "Thu, 03 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.10463402652693643,
                  "trade_date": "Wed, 02 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.09685606680858039,
                  "trade_date": "Tue, 01 Mar 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.10749959063369896,
                  "trade_date": "Mon, 28 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.0966104470280007,
                  "trade_date": "Fri, 25 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.09726543310954638,
                  "trade_date": "Thu, 24 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.07810709022433282,
                  "trade_date": "Wed, 23 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.0704928770263632,
                  "trade_date": "Tue, 22 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.04519403962665802,
                  "trade_date": "Mon, 21 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": -0.022105780252169804,
                  "trade_date": "Fri, 18 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.027100049123956138,
                  "trade_date": "Thu, 17 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.029556246929752783,
                  "trade_date": "Wed, 16 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.024480104797773183,
                  "trade_date": "Tue, 15 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.01326346815130175,
                  "trade_date": "Mon, 14 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.02611757000163739,
                  "trade_date": "Fri, 11 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.046913378090715385,
                  "trade_date": "Thu, 10 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.05084329457999015,
                  "trade_date": "Wed, 09 Feb 2022 00:00:00 GMT"
                },
                {
                  "income_rate": 0.014000327493040698,
                  "trade_date": "Tue, 08 Feb 2022 00:00:00 GMT"
                }
              ],
              "extra_data": null,
              "msg": "success"
            }
        ---
        """
        data = request.args
        fund_id, interval = data.get('fund_id'), data.get('interval', 30, type=int)
        res, count = get_fund_dynamic_rate_trend(fund_id, interval)
        return sx_json(200, res)


def get_fund_detail(fund_id):
    """跟据fund_id 获取 基金详情"""
    res = {}
    fund_desc = get_fund_desc(fund_id)
    res.update(fund_desc)
    fund_index_info = get_fund_index_info(fund_id)
    res.update(fund_index_info)

    return res


def get_fund_list(page_id, page_size):
    """根据页码，页量获取对应基金信息"""
    res = []
    fund_navs = get_fund_nav_list(page_id, page_size)
    for fun_nav in fund_navs:
        fund_detail = get_fund_detail(fun_nav.fund_id)
        fund_detail.update(fun_nav.to_msg())
        res.append(fund_detail)

    return res


def get_fund_income_rate_trend(fund_id, interval):
    """获取基金的业绩走势"""
    res = []
    fund_nav_trend = get_fun_nav_interval_trend(fund_id, interval)
    start_fund = fund_nav_trend[-1]
    for fund_nav in fund_nav_trend[:-1]:
        trade_date = fund_nav.trade_date
        income_rate = fund_nav.nav_unit / start_fund.nav_unit - 1 if start_fund.nav_unit else 0
        res.append(dict(trade_date=trade_date, income_rate=income_rate))
    return res, len(res)


def get_fund_dynamic_rate_trend(fund_id, interval):
    """获取基金的动态回撤曲线"""
    res = []
    fund_nav_trend = get_fun_nav_interval_trend(fund_id, interval)
    fund_nav_trend.reverse()
    max_nav_unit = fund_nav_trend[0].nav_unit
    for fund_nav in fund_nav_trend[1:]:
        trade_date = fund_nav.trade_date
        income_rate = fund_nav.nav_unit / max_nav_unit - 1 if max_nav_unit else 0
        max_nav_unit = max(fund_nav.nav_unit, max_nav_unit)
        res.append(dict(trade_date=trade_date, income_rate=income_rate))
    return res, len(res)


@fund_func.route("/cache_data")
class CacheCsvData(Resource):
    def get(self):
        # CacheData.update_desc_data()
        CacheData.update_nv_data()

