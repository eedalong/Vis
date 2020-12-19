import requests
import json
################################################################
# run this project by: python manage.py runserver 0.0.0.0:8001 #
################################################################


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

res = requests.get("http://0.0.0.0:8001/product/sell/", params={"batch_number":"BJ38668", "year": 2018, "month": 8, "province": "山东省"})
print(json.loads(res.content.decode()))
