import networkx as nx
import matplotlib.pyplot as plt

from PageRank.construct_edges import ConstructEdges
from invertedIndex.inverted_index import Index


class PageRank:
    def __init__(self, edges = []):
        self.pagerank_list = []
        self.pg_edges = edges
    def compute_pagerank(self):
        #有向图G
        G = nx.DiGraph()
        for edge in self.pg_edges:
            G.add_edge(edge[0], edge[1])

        nx.draw(G, with_labels=True)
        plt.show()
        self.pagerank_list = nx.pagerank(G, alpha=0.85)

if __name__ == '__main__':
    # build index
    my_index = Index()
    my_index.docs_read_and_build_index("../dataset/")
    # construct edges
    construt_edge = ConstructEdges(my_index.doc_list)
    construt_edge.construct_matrix_and_edges()
    # pagerank
    my_page_rank = PageRank(construt_edge.edges)
    my_page_rank.compute_pagerank()
    print("pagerank:\n", my_page_rank.pagerank_list)
    pass

