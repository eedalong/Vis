from Vis.service import DrugFlow, SellPredictor
#######################
#  For a dealer       #
#######################
res = DrugFlow.flow("BJ45743", "BY100002")
#######################
#  For province       #
#######################
res = DrugFlow.flow_province("BJ45743", "福建省")

###########################
#   Get Sells Data        #
###########################
#   Get Province Sell Data#
###########################
sells = SellPredictor()
sell_res = sells.sell_province("BJ38668", 2018, 6)

##############################
# Get City Sell In A Province#
##############################
sell_res = sells.sell_city("BJ38668", 2018, 6, "山东省")

print(sell_res)


