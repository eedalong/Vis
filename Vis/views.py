from django.shortcuts import render
from codex.baseview import APIView
from Vis.service import  DrugFlow
# Create your views here.

class Flow(APIView):
    def get(self):
        self.check_input("batch_number", "starter")
        return DrugFlow.flow(self.input["batch_number"], self.input["starter"])

