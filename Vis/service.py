from backend.db_conn import *
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class DrugFlow:
    @classmethod
    def flow(cls, batch, starter, day_range=30):
        res = drug_sale(batch=batch)
        candidates = []
        for index, record in enumerate(res):
            if record[1] == starter:
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
        return return_res



        '''
        g = nx.Graph()
        all_nodes = set([])
        for index in candidates:
            record = res[index]
            g.add_edge(record[1], record[4])
            all_nodes.add(record[1])
            all_nodes.add(record[4])

        nx.draw(g)
        plt.show()
        '''
