# 构建倒排索引
import array
import os
import re
import jieba
import math

# def encode(postings_list):
#     """Encodes postings_list into a stream of bytes
#
#     Parameters
#     ----------
#     postings_list: List[int]
#         List of docIDs (postings)
#
#     Returns
#     -------
#     bytes
#         bytearray representing integers in the postings_list
#     """
#     return array.array('L', postings_list).tobytes()
#
#
#
# def decode(encoded_postings_list):
#     """Decodes postings_list from a stream of bytes
#
#     Parameters
#     ----------
#     encoded_postings_list: bytes
#         bytearray representing encoded postings list as output by encode
#         function
#
#     Returns
#     -------
#     List[int]
#         Decoded list of docIDs from encoded_postings_list
#     """
#
#     decoded_postings_list = array.array('L')
#     decoded_postings_list.frombytes(encoded_postings_list)
#     return decoded_postings_list.tolist()

class MyDoc:
    def __init__(self):
        self.id = ""
        self.title = ""
        self.url = ""
        self.content = ""
    def addId(self, value):
        self.id = value
    def addTitle(self, value):
        self.title = value
    def addUrl(self, value):
        self.url = value
    def addContent(self, value):
        self.content = value

    def getId(self):
        return self.id
    def getTitle(self):
        return self.title
    def getUrl(self):
        return self.url
    def getContent(self):
        return self.content



class Index:
    def __init__(self):
        self.doc_list = []
        self.term_list = []
        self.inverted = {}
        self.idf = {}

    def getDocList(self):
        return self.doc_list
    def getTermList(self):
        return self.term_list
    def getInverted(self):
        return self.inverted
    def getIdf(self):
        return self.idf

    # 创建停用词列表
    def stop_words_list(self):
        stop_words = [line.strip() for line in open("stop_words.txt", encoding='UTF-8').readlines()]
        return stop_words

    # 对句子进行中文分词
    def depart_words(self,doc):
        doc_depart = jieba.cut_for_search(doc.getContent())
        stop_words = self.stop_words_list()
        # 输出结果为outstr
        out_list = []
        # 去停用词
        for word in doc_depart:
            if word not in stop_words:
                if word != '\t':
                    out_list.append(word)
        return out_list

    def docs_read_and_build_index(self, filedir_path):
        doc_name_list = os.listdir(filedir_path)
        #文档路径列表
        doc_path_list = []
        for doc_name in doc_name_list:
            doc_path = os.path.join(filedir_path,doc_name)
            doc_path_list.append(doc_path)

        for doc_path in doc_path_list:
            with open(doc_path, 'r', encoding='utf-8') as doc_file:
                doc = MyDoc()
                first_line = doc_file.readline()
                id, title, url = first_line.split('\t')
                doc.addId(id)
                doc.addTitle(title)
                doc.addUrl(url[0:-1])
                others_line = doc_file.read()#from line 2?
                others_line = others_line.replace("\n", " ")
                others_line = others_line.replace("。", " ")
                others_line = others_line.replace("，", " ")
                others_line = others_line.replace("！", " ")
                others_line = others_line.replace("？", " ")
                others_line = others_line.replace(",", " ")
                others_line = others_line.replace("!", " ")
                others_line = others_line.replace("?", " ")
                doc.addContent(others_line)
                self.doc_list.append(doc)
        self.inverted_index()

    def inverted_index(self):
        doc_list_len = len(self.doc_list)
        # inverted index
        for doc in self.doc_list:
            id = doc.getId()
            # 倒排索引
            this_term_list = self.depart_words(doc)#分词
            #本轮词项集合加入索引词项词典（去重）
            self.term_list.extend(this_term_list)
            self.term_list = list(set(self.term_list))
            #用本轮词项集合扩充索引（不去重要计数tf）
            for t in this_term_list:
                if t in self.inverted:
                    if id not in self.inverted[t]:
                        self.inverted[t][id] = 1
                    else:
                        self.inverted[t][id] += 1
                else:
                    self.inverted[t] = {id: 1}
            print("building doc id=%s" % id)
        # idf
        for t in self.inverted:
            self.idf[t] = math.log10(doc_list_len / len(self.inverted[t]))
        # # write to disk
        # with open("index_dir/inverted_index.txt", 'w', encoding='utf-8') as index_file:
        #     temp_list = list(self.inverted)
        #     index_file.write(encode(temp_list))
        # with open("index_dir/term_list.txt", 'w', encoding='utf-8') as term_list_file:
        #     temp_list = list(self.term_list)
        #     term_list_file.write(encode(temp_list))
        # with open("idf_dir/idf.txt", 'w', encoding='utf-8') as idf_file:
        #     temp_list = list(self.idf)
        #     idf_file.write(encode(temp_list))

        print("inverted terms:%d" % len(self.inverted))
        print("index done")




if __name__ == '__main__':
    # build index
    my_index = Index()
    my_index.docs_read_and_build_index("../dataset/")
