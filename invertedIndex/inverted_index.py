# 构建倒排索引
import array
import os
import re
import jieba
import math

from other_tools.process_bar import process_bar


class MyDoc:
    def __init__(self):
        self.id = 0
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
        # 每篇文档中的pos_term
        self.pos_term = []
        # 每篇文档中词项和其位置列表映射
        self.term_poslist = {}

    def getDocList(self):
        return self.doc_list
    def getTermList(self):
        return self.term_list
    def getInverted(self):
        return self.inverted

    # 创建停用词列表
    def stop_words_list(self):
        stop_words = [line.strip() for line in open("../invertedIndex/stop_words.txt", encoding='UTF-8').readlines()]
        return stop_words

    # 对句子进行中文分词
    def depart_words(self, doc):
        doc_depart = jieba.cut_for_search(doc.getContent())
        stop_words = self.stop_words_list()
        # 输出结果为outstr
        out_list = []
        pos = 1
        # 去停用词
        for word in doc_depart:
            if word not in stop_words:
                if word != '\t':
                    out_list.append(word)
                    self.pos_term.append((pos, word)) # 记录位置
                    pos = pos + 1
        return out_list

    # 外部使用
    def extern_depart_words(self, doc):
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

    # 建立词项和其位置列表映射
    def build_term_poslist(self):
        for pos, term in self.pos_term:
            postions = self.term_poslist.setdefault(term, [])
            postions.append(pos)

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
                sid, title, url = first_line.split('\t')
                doc.addId(int(sid))
                doc.addTitle(title)
                doc.addUrl(url[0:-1])
                others_line = doc_file.read()
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
        self.doc_list.sort(key=lambda x:x.id)
        self.inverted_index()

    def inverted_index(self):
        doc_list_len = len(self.doc_list)
        # inverted index
        for doc in self.doc_list:
            id = doc.getId()
            # 分词
            this_term_list = self.depart_words(doc)
            self.build_term_poslist()
            #本轮词项集合加入索引词项词典（去重）
            self.term_list.extend(this_term_list)
            self.term_list = list(set(self.term_list))
            # 用本轮词项集合扩充索引（不去重要记录位置）
            for t in this_term_list:
                if t in self.inverted:
                    if id not in self.inverted[t]:
                        self.inverted[t][id] = self.term_poslist[t]
                    else:
                        pass
                else:
                    self.inverted[t] = {id: self.term_poslist[t]}

            process_bar(id + 1, doc_list_len)
            self.term_poslist = {}
            self.pos_term = []


