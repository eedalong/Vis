from backend.db_conn import *
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List
class DrugFlow:
    @classmethod
    def flow(cls, batch:str, starters:List[str], day_range=30):
        res = drug_sale(batch=batch)
        candidates = []
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
        return return_res

    @classmethod
    def flow_province(cls, batch, province):
        dealers = get_dealers_province(province)
        starters = [item[0] for item in dealers]
        res = cls.flow(batch, starters)
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
