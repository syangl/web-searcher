# coding:utf-8
from flask import Flask, request, render_template, redirect, url_for

from PageRank.construct_edges import ConstructEdges
from PageRank.page_rank import PageRank
from invertedIndex.inverted_index import Index
from query.query import Querier

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query = query))
    elif request.method == 'POST' and request.form.get('phrase_query'):
        query = request.form['phrase_query']
        return redirect(url_for('phrase_search', query = query))
    elif request.method == 'POST' and request.form.get('wildcard_query'):
        query = request.form['wildcard_query']
        return redirect(url_for('wildcard_search', query = query))
    elif request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('login', username = username, password = password))

    return render_template('index.html')

@app.route("/search/<query>", methods=['POST', 'GET'])
def search(query):
    sorted_result = my_query.search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for id in docs_id:
        docs_list.append(my_index.doc_list[int(id)])
    return render_template('search.html', docs_list = docs_list, value = query, length = len(docs_list))

@app.route("/phrase_search/<query>", methods=['POST', 'GET'])
def phrase_search(query):
    sorted_result = my_query.phrase_search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for id in docs_id:
        docs_list.append(my_index.doc_list[int(id)])
    return render_template('search.html', docs_list = docs_list, value = query, length = len(docs_list))

@app.route("/wildcard_search/<query>", methods=['POST', 'GET'])
def wildcard_search(query):
    sorted_result = my_query.wildcard_search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for id in docs_id:
        docs_list.append(my_index.doc_list[int(id)])
    return render_template('search.html', docs_list = docs_list, value = query, length = len(docs_list))

@app.route("/login/<username>&<password>", methods=['POST', 'GET'])
def login(username, password):
    # TODO: 账号登录，注册账号的步骤就简单化处理不用数据库了，因为只需要用户名和密码，这部分也和作业内容关系不大，用户名存在检查密码，不存在注册新用户）

    # 如果密码正确
    return redirect(url_for('logined_index', username = username))

@app.route("/logined_index/<username>", methods=['POST', 'GET'])
def logined_index(username):
    if request.method == 'POST' and request.form.get('login_query'):
        query = request.form['login_query']
        return redirect(url_for('search', query = query))
    elif request.method == 'POST' and request.form.get('login_phrase_query'):
        query = request.form['login_phrase_query']
        return redirect(url_for('phrase_search', query = query))
    elif request.method == 'POST' and request.form.get('login_wildcard_query'):
        query = request.form['login_wildcard_query']
        return redirect(url_for('wildcard_search', query = query))

    return render_template('logined_index.html', username=username)




my_index = Index()
my_query = Querier(my_index, None)

if __name__ == '__main__':
    # build index
    print("building inverted index...")
    my_index.docs_read_and_build_index("dataset/")
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
    print("\ncomputing PageRank done\nset my_query...\n")
    # init my_query
    my_query.set_index(my_index)
    my_query.set_page_rank(my_page_rank.pagerank_dict)
    print("set my_query done")

    app.run(host='localhost', port=8080, debug=True)