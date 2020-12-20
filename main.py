import requests
import json
from Vis.service import position
################################################################
# run this project by: python manage.py runserver 0.0.0.0:8001 #
################################################################

##########################################
#     CACHE CITY COORDINATION            #
##########################################

cache_res = {}
with open("city.json") as city_json:
    citys = json.load(city_json)
    for city in citys:
        res = position(city)
        cache_res[city] = res
    json.dump(cache_res, open("cache.json", "w", encoding="utf8"))







#######################
#  For a dealer       #
#######################
res = requests.get("http://0.0.0.0:8001/flow", params={"batch_number":"BJ45743", "starter":"BY100002"})
print(json.loads(res.content.decode()))

#################
# Get Sell Data #
#################
res = requests.get("http://0.0.0.0:8001/product/sell/", params={"batch_number":"BJ38668", "year": 2018, "month": 8, "province": ""})
print(json.loads(res.content.decode()))

res = requests.get("http://0.0.0.0:8001/risk/cycle/", params={"batch_number":"BJ31436"})
print(json.loads(res.content.decode()))
