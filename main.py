from Vis.service import DrugFlow
import networkx as nx
import matplotlib.pyplot as plt
#######################
#  For a dealer       #
#######################
res = DrugFlow.flow("BJ45743", "BY100002")
#######################
#  For province       #
#######################
#res = DrugFlow.flow_province("BJ45743", "福建省")

g = nx.Graph()
for item in res:
    g.add_edge(item[1], item[4])

nx.draw(g)
plt.show()