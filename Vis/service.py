from backend.db_conn import *
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List
import requests
import fire
import random
def position(name):
    url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=vGXMdnaoFupqsBYi8AUbN9lzvCzbmQIo'%(name)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        if val["status"] == 0:
            retval = {'地址':name,'经度':val['result']['location']['lng'],'纬度':val['result']['location']['lat'],'地区标签':val['result']['level'],'是否精确查找':val['result']['precise']}
        else:
            retval = None
        return retval
    else:
        print('无法获取%s经纬度'%name)

class DrugFlow:
    @classmethod
    def flow(cls, batch:str, *starters, day_range=30):
        res = drug_sale(batch=batch)
        candidates = []
        all_city = set([])
        for index, record in enumerate(res):
            if record[1] in starters:
                candidates.append(index)
        def recursiveFind(idx_res):
            current = res[idx_res]
            for index in range(idx_res+1, len(res)):
                if current[4] == res[index][1] and res[index][0]-current[0] < timedelta(days=day_range):
                    candidates.append(index)
                    recursiveFind(index)
        candidate_length = len(candidates)
        for i in range(candidate_length):
            recursiveFind(candidates[i])
        return_res = []
        for idx in candidates:
            return_res.append(res[idx])
        return_res.sort(key=lambda x:x[0])
        for index in range(len(return_res)):
            # process coordination
            pos_res = position(return_res[index][3])
            pos = [pos_res["经度"], pos_res["纬度"]]
            if return_res[index][3] in all_city:
                pos = [pos[0] - random.random(), pos[1] + random.random()]
            return_res[index].append(pos)
            # process datetime
            try:
                return_res[index][0] = return_res[index][0].strftime("%Y-%m-%d")
            except:
                pass
        return return_res

    @classmethod
    def flow_province(cls, batch, province):
        dealers = get_dealers_province(province)
        starters = [item[0] for item in dealers]
        res = cls.flow(batch, *starters)
        for item in res:
            if item[1] in starters:
                item[1] = "province"
            if item[4] in starters:
                item[4] = "province"
        return res


class Dealer:
    @classmethod
    def get_dealers_from_city(cls, city):
        return get_dealers_city(city)

    @classmethod
    def get_dealers_from_province(cls, province):
        return get_dealers_province(province)

class SellPredictor:
    all_years = [2017, 2018, 2019]
    @classmethod
    def sell_province(cls, batch_number, year, month):
        return drug_amount_province(batch=batch_number, year=year, month=month)

    @classmethod
    def sell_city(cls, batch_number, year, month, province):
        return drug_amount_city(batch=batch_number, year=year, month=month, province=province)


    @classmethod
    def predict_dealer(cls):
        pass
    @classmethod
    def predict_city(cls):
        pass
    @classmethod
    def predict_province(cls):
        pass

    @classmethod
    def predict_country(cls):
        pass

