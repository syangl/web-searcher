import jieba

from PageRank.construct_edges import ConstructEdges
from PageRank.page_rank import PageRank
from invertedIndex.inverted_index import Index


class Querier:
    def __init__(self, idx, pg):
        self.index = idx
        self.page_rank = pg
    def query(self, q):
        term_list = []
        q = q.split(" ")
        for it in q:
            term_list.append(it)

        num_pg = {}
        for term in term_list:
            # TODO：多个查询词怎么判断谁重要？ 或许可以配合高级检索功能
            if term in self.index.inverted:
                doc_list = self.index.inverted[term].items()
                for it in doc_list:
                    num_pg[str(it[0])] = self.page_rank[str(it[0])]

        sorted_docs_list = sorted(num_pg.items(), key = lambda x:x[1], reverse = True)
        return sorted_docs_list

# if __name__ == '__main__':
#     # build index
#     print("building inverted index...")
#     my_index = Index()
#     my_index.docs_read_and_build_index("../dataset/")
#     print("\nbuilding inverted index done")
#     # construct edges
#     print("constructing matrix and edges...")
#     construt_edge = ConstructEdges(my_index.doc_list)
#     construt_edge.construct_matrix_and_edges()
#     print("\nconstructing matrix and edges done")
#     # pagerank
#     print("computing PageRank...")
#     my_page_rank = PageRank(construt_edge.edges)
#     my_page_rank.compute_pagerank()
#     print("\nPageRank is:\n", my_page_rank.pagerank_dict)
#     # query
#     q = input("input your qeury terms:\n")
#     my_query = Querier(my_index, my_page_rank.pagerank_dict)
#     res = my_query.query(q)
#     print("query result:\n", res)
#     pass

