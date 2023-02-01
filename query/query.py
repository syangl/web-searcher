import jieba

from PageRank.construct_edges import ConstructEdges
from PageRank.page_rank import PageRank
from invertedIndex.inverted_index import Index, MyDoc


class Querier:
    def __init__(self, idx, pg):
        self.index = idx
        self.page_rank = pg

    def set_index(self, idx):
        self.index = idx

    def set_page_rank(self, pg):
        self.page_rank = pg

    def search(self, query):
        '''
        站内查询
        :param query: 查询词
        :return: 包含所有查询词的文档
        '''
        term_list = []
        query = query.split(" ")
        for it in query:
            term_list.append(it)

        num_pg = {}
        for term in term_list:
            if term in self.index.inverted.keys():
                doc_list = self.index.inverted[term].items()
                for it in doc_list:
                    num_pg[str(it[0])] = self.page_rank[str(it[0])]


        sorted_docs_list = sorted(num_pg.items(), key = lambda x:x[1], reverse = True)
        return sorted_docs_list

    def phrase_search(self, query):
        '''
        短语查询
        :param query: 查询词
        :return:包含查询短语的结果
        '''
        qeury_list = []
        query_doc = MyDoc()
        query_doc.addContent(query)
        qeury_list = Index().extern_depart_words(query_doc)
        if " " in qeury_list:
            qeury_list.remove(" ")

        result = []
        sorted_result = []
        if len(qeury_list) > 1:
            temp_dict = {}
            for i in range(0, len(qeury_list)):
                if qeury_list[i] in self.index.inverted.keys():
                    temp_docs = self.index.inverted[qeury_list[i]].keys()
                    temp_dict.setdefault(i, temp_docs)
            temp_dict_new = temp_dict[0]
            for i in range(1, len(qeury_list)):
                temp_dict_new = [val for val in temp_dict_new if val in temp_dict[i]]
            for key in temp_dict_new:
                first_poslist = self.index.inverted[qeury_list[0]][key]
                judge_list = []
                for pos in first_poslist:
                    judge_per_list = []
                    for j in range(1, len(qeury_list)):
                        if pos + j not in self.index.inverted[qeury_list[j]][key]:
                            judge_per_list.append(0)
                        else:
                            judge_per_list.append(1)

                    if 0 in judge_per_list:
                        judge_list.append(0)
                    else:
                        judge_list.append(1)
                if 1 in judge_list:
                    result.append(key)
            # pagerank
            num_pg = {}
            for id in result:
                num_pg[str(id)] = self.page_rank[str(id)]

            sorted_result = sorted(num_pg.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_result = self.search(query)
        
        return sorted_result


    def wildcard_search(self, query):
        '''
        通配查询
        :param query: 查询词
        :return: 通配查询结果
        '''
        result = []
        sorted_result = []
        if '*' in query and ' ' not in query:
            length = len(query) - 1
            pos = query.index('*')
            if pos == 0:
                # head
                query_term = query[1:]
                for term in self.index.inverted.keys():
                    idx_term = term[-length:]
                    if query_term == idx_term:
                        result.extend( self.index.inverted[term].keys())
                # pagerank
                num_pg = {}
                for id in result:
                    num_pg[str(id)] = self.page_rank[str(id)]
                sorted_result = sorted(num_pg.items(), key=lambda x: x[1], reverse=True)
            elif pos == length:
                # tail
                query_term = query[:-1]
                for term in self.index.inverted.keys():
                    idx_term = term[:length]
                    if query_term == idx_term:
                        result.extend(self.index.inverted[term].keys())
                # pagerank
                num_pg = {}
                for id in result:
                    num_pg[str(id)] = self.page_rank[str(id)]
                sorted_result = sorted(num_pg.items(), key=lambda x: x[1], reverse=True)
            else:
                # middle
                query_split = query.split('*')
                query_term1 = query_split[0]
                query_term2 = query_split[1]
                len1 = len(query_term1)
                len2 = len(query_term2)
                for term in self.index.inverted.keys():
                    idx_term1 = term[:len1]
                    idx_term2 = term[-len2:]
                    if query_term1 == idx_term1 and query_term2 == idx_term2 and len(term) >= (len1 + len2):
                        result.extend(self.index.inverted[term].keys())
                # pagerank
                num_pg = {}
                for id in result:
                    num_pg[str(id)] = self.page_rank[str(id)]
                sorted_result = sorted(num_pg.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_result = self.search(query)

        return sorted_result
