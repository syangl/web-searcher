from PageRank.construct_edges import ConstructEdges
from PageRank.page_rank import PageRank
from invertedIndex.inverted_index import Index
from query.query import Querier

if __name__ == '__main__':
    # build index
    print("building inverted index...")
    my_index = Index()
    my_index.docs_read_and_build_index("../dataset/")
    print("\nbuilding inverted index done")
    # construct edges
    print("constructing matrix and edges...")
    construt_edge = ConstructEdges(my_index.doc_list)
    construt_edge.construct_matrix_and_edges()
    print("\nconstructing matrix and edges done")
    # pagerank
    print("computing PageRank...")
    my_page_rank = PageRank(construt_edge.edges)
    my_page_rank.compute_pagerank()
    print("\nPageRank is:\n", my_page_rank.pagerank_dict)
    # query
    q = input("input your qeury terms:\n")
    my_query = Querier(my_index, my_page_rank.pagerank_dict)
    res = my_query.query(q)
    print("query result:\n", res)
    pass