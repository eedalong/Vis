from django.shortcuts import render
from codex.baseview import APIView
from Vis.service import  DrugFlow, SellPredictor, RiskDetector
# Create your views here.

class Flow(APIView):
    def get(self):
        self.check_input("batch_number", "starter")
        return DrugFlow.flow(self.input["batch_number"], self.input["starter"])

class ProductSale(APIView):
    def get(self):
        self.check_input("batch_number", "year", "month", "province")
        batch, year, month, province = self.input["batch_number"], self.input["year"], self.input["month"], self.input["province"]
        if province:
            return SellPredictor.sell_city(batch_number=batch, year=year, month=month, province=province)
        else:
            return SellPredictor.sell_province(batch_number=batch, year=year, month=month)

class Risk(APIView):
    def get(self):
        self.check_input("query_area")
        query_area = self.input["query_area"]
        res = RiskDetector.risk_area(query_area)
        return res

class CycleRisk(APIView):
    def get(self):
        self.check_input("batch_number")
        res = RiskDetector.risk_multi(self.input["batch_number"])
        return res