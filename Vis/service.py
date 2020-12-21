from backend.db_conn import *
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List
import requests
import fire
import random
import json
import time

def position(name):
    url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=znaraUep880G8Nsc4v3yfkGd4ZIjbNKE'%(name)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        if val["status"] == 0:
            retval = {
                '地址': name,
                '经度': val['result']['location']['lng'],
                '纬度': val['result']['location']['lat'],
                '地区标签': val['result']['level'],
                '是否精确查找': val['result']['precise']
            }
        else:
            retval = None
        return retval
    else:
        print('无法获取%s经纬度' % name)

def pos_cache(name):
    cache = json.load(open("cache.json"))
    if not cache.get(name, None):
        return position(name)
    return cache[name]

class DrugFlow:
    @classmethod
    def flow(cls, batch:str, *starters, day_range=30):
        start = time.time()
        res = drug_sale(batch=batch)
        start = time.time()

        candidates = []
        pos_dict = {}
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
            # process seller coordination
            pos_res = pos_cache(return_res[index][3])
            pos = [pos_res["经度"], pos_res["纬度"]]
            if return_res[index][3] in all_city:
                pos = [pos[0] - 2 * random.choice([1, -1]) * random.random(), pos[1] + 2 *random.random()]
            pos = pos_dict.get(return_res[index][1], None) or pos

            pos_dict[return_res[index][1]] = pos
            return_res[index].append(pos)
            all_city.add(return_res[index][3])

            # process buyer coordination
            pos_res = pos_cache(return_res[index][6])
            pos = [pos_res["经度"], pos_res["纬度"]]
            if return_res[index][6] in all_city:
                pos = [pos[0] - random.choice([1, -1]) * random.random(), pos[1] + 2 * random.random()]
            pos = pos_dict.get(return_res[index][4], None) or pos

            pos_dict[return_res[index][4]] = pos
            return_res[index].append(pos)
            all_city.add(return_res[index][6])
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
        res = drug_amount_province(batch=batch_number, year=year, month=month)
        for index in range(len(res)):
            pos_res = pos_cache(res[index][0])
            pos = [pos_res["经度"], pos_res["纬度"]]
            res[index].append(pos)
        return res

    @classmethod
    def sell_city(cls, batch_number, year, month, province):
        res = drug_amount_city(batch=batch_number, year=year, month=month, province=province)
        for index in range(len(res)):
            pos_res = pos_cache(res[index][0])
            pos = [pos_res["经度"], pos_res["纬度"]]
            res[index].append(pos)
        return res


    @classmethod
    def predict_dealer(cls,dealer_id):
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


class RiskDetector:
    @classmethod
    def risk_area(cls, query_area=None):
        risk_value = risk_area()
        risk_value = {
            area_name: {
                province_name: {
                    city_name: city['risk_value'] for city_name, city in province.items() if type(city) != int
                } for province_name, province in area.items() if type(province) != int
            } for area_name, area in risk_value.items()
        }
        if query_area in [None, '']:
            return risk_value
        else:
            return risk_value[query_area]

    @classmethod
    def risk_multi(cls, batch):
        start = time.time()
        with open("risk_batch.json") as risk_batch_file:
            risk_batch = json.load(risk_batch_file)
            agents = risk_batch["multi-cycle"][batch]
            all_data = drug_sale(batch)
            starter = None
            for item in all_data:
                if item[1] in agents:
                    starter = item[1]
                    break
        res = DrugFlow.flow(batch, starter)
        res = list(filter(lambda x: x[1] in agents and x[4] in agents, res))
        res.append(agents)
        print("check total time ", time.time() - start)
        return res





