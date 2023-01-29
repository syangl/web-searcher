import math
import os
import numpy as np
from  invertedIndex.inverted_index import Index
from other_tools.process_bar import process_bar


class ConstructEdges:

    def __init__(self, index_doc_list = []):
        self.ce_doc_list = index_doc_list
        self.edges = []
        self.PR_matrix = np.zeros((len(index_doc_list),len(index_doc_list)))

    @staticmethod
    def list_intersect(list1, list2):
        '''
        :param list1:
        :param list2:
        :return: 求交去重
        '''
        merge_list = []
        curr1 = 0
        curr2 = 0
        while curr1 < len(list1) and curr2 < len(list2):
            if list1[curr1] == list2[curr2]:
                merge_list.append(list1[curr1])
                curr1 += 1
                curr2 += 1
            elif list1[curr1] < list2[curr2]:
                curr1 += 1
            elif list1[curr1] > list2[curr2]:
                curr2 += 1
        return list(set(merge_list))

    def compute_PR(self, doc1, doc2):
        '''
        :param doc1:
        :param doc2:
        :return: doc1到doc2的外链值
        '''
        doc1_term_list = Index().depart_words(doc1)
        doc2_term_list = Index().depart_words(doc2)
        intersect_list = self.list_intersect(doc1_term_list, doc2_term_list)
        PR_1to2 = 0
        for term in intersect_list:
            cnt1 = doc1_term_list.count(term)
            cnt2 = doc2_term_list.count(term)
            PR_1to2 += math.tan(cnt1/cnt2)
        return PR_1to2

    def construct_matrix_and_edges(self):
        n = len(self.ce_doc_list)
        for_cnt = 0
        total = n * n
        for i in range(0,n):
            for j in range(0,n):
                self.PR_matrix[i][j] = self.compute_PR(self.ce_doc_list[i], self.ce_doc_list[j])
                if self.PR_matrix[i][j] != 0:
                    self.edges.append((str(i), str(j)))
                for_cnt += 1
                process_bar(for_cnt, total)

# if __name__ == '__main__':
# #     # build index
# #     my_index = Index()
# #     my_index.docs_read_and_build_index("../dataset/")
# #     # construct edges
# #     construt_edge = ConstructEdges(my_index.doc_list)
# #     construt_edge.construct_matrix_and_edges()
# #     print(construt_edge.PR_matrix)
# #     print(construt_edge.edges)



