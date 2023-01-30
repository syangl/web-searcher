import networkx as nx
import matplotlib.pyplot as plt

from PageRank.construct_edges import ConstructEdges
from invertedIndex.inverted_index import Index
from other_tools.process_bar import process_bar


class PageRank:
    def __init__(self, edges = []):
        self.pagerank_dict = {}
        self.pg_edges = edges
    def compute_pagerank(self):
        pg_edges_len = len(self.pg_edges)
        for_cnt = 0
        #有向图G
        G = nx.DiGraph()
        for edge in self.pg_edges:
            G.add_edge(edge[0], edge[1])
            for_cnt += 1
        process_bar(for_cnt, pg_edges_len)

        # nx.draw(G, with_labels=True)
        # plt.show()
        self.pagerank_dict = nx.pagerank(G, alpha=0.85)

