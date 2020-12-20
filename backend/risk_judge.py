import json
import numpy as np





class BatchGraph:
    def __init__(self, batch_number, batch):
        self.batch_number = batch_number
        agents = batch['agents']
        edges = batch['edges']
        self.agents = agents
        self.n = len(agents)
        self.agent_ph_mapping = {
            agent: i for i, agent in enumerate(agents)
        }
        self.adjacency = np.zeros((self.n, self.n), dtype=np.int32)
        for edge in edges:
            start = self.agent_ph_mapping[edge[0]]
            end = self.agent_ph_mapping[edge[1]]
            self.adjacency[start, end] = 1

    def pow(self):
        powers = []
        i = 1
        powers.append(self.adjacency)
        while True:
            if i * 2 > self.n:
                break
            prod = np.matmul(powers[-1], powers[-1])
            prod[prod > 0] = 1
            powers.append(prod)
            i *= 2
        n = self.n

        powad = np.identity(self.n)
        i = 0
        while n > 0:
            if n & 1 == 1:
                powad = np.matmul(powad, powers[i])
            n >>= 1
            i += 1
        return powad


def risk_judge(sale):
    # sc_agent = set()
    risk_batch = {
        'self-cycle': {},
        'multi-cycle': {}
    }
    nbatches = len(sale)
    graphs = []
    print('Load data')
    for i, (batch_number, batch) in enumerate(sale.items()):
        if batch_number == 'null':
            continue
        graphs.append(BatchGraph(batch_number, batch))

    # self-cycle
    print('-' * 80)
    print('Detect Self-cycle')
    for i, graph in enumerate(graphs):
        if i % 100 == 0:
            print(f'Batch {i}/{nbatches}')
        sc_slice = np.where(np.diagonal(graph.adjacency) > 0)[0]
        if sc_slice.size > 0:
            risk_batch['self-cycle'][graph.batch_number] = [graph.agents[sc_id] for sc_id in sc_slice]
        # remove self-cycle
        for j in range(graph.n):
            graph.adjacency[j, j] = 0

    # multi-cycle
    print('-' * 80)
    print('Detect Multi-cycle')
    for i, graph in enumerate(graphs):
        if i % 100 == 0:
            print(f'Batch {i}/{nbatches}')
        if graph.n > 1:
            powad = graph.pow()
            mc_slice = np.where(np.diagonal(powad) > 0)[0]
            if mc_slice.size > 0:
                risk_batch['multi-cycle'][graph.batch_number] = [graph.agents[sc_id] for sc_id in mc_slice]
    return risk_batch
