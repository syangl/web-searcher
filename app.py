# coding:utf-8
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for

from PageRank.construct_edges import ConstructEdges
from PageRank.page_rank import PageRank
from invertedIndex.inverted_index import Index
from other_tools.delete_files import del_files
from query.query import Querier

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query, is_login=False, username=None))
    elif request.method == 'POST' and request.form.get('phrase_query'):
        query = request.form['phrase_query']
        return redirect(url_for('phrase_search', query=query, is_login=False, username=None))
    elif request.method == 'POST' and request.form.get('wildcard_query'):
        query = request.form['wildcard_query']
        return redirect(url_for('wildcard_search', query=query, is_login=False, username=None))
    elif request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('login', username=username, password=password))

    return render_template('index.html')


@app.route("/search/<query>&<is_login>&<username>", methods=['POST', 'GET'])
def search(query, is_login, username):
    if request.method == 'POST' and request.form.get('cache'):
        cache_value = request.form['cache']
        id_str = cache_value[2:]
        return redirect(url_for('cache', id_str=id_str))
    sorted_result = my_query.search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for i in docs_id:
        docs_list.append(my_index.doc_list[int(i)])
    if is_login and (username is not None):
        writefile = open("SearchLog/" + username + ".log", 'a', encoding='UTF-8')
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        writefile.write("[" + time + "] " + "search_mode:search " + username + " " + query + "\n")
        writefile.close()
    return render_template('search.html', docs_list=docs_list, value=query, length=len(docs_list))


@app.route("/phrase_search/<query>&<is_login>&<username>", methods=['POST', 'GET'])
def phrase_search(query, is_login, username):
    if request.method == 'POST' and request.form.get('cache'):
        cache_value = request.form['cache']
        id_str = cache_value[2:]
        return redirect(url_for('cache', id_str=id_str))
    sorted_result = my_query.phrase_search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for i in docs_id:
        docs_list.append(my_index.doc_list[int(i)])
    if is_login and (username is not None):
        writefile = open("SearchLog/" + username + ".log", 'a', encoding='UTF-8')
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        writefile.write("[" + time + "] " + "search_mode:phrase_search " + username + " " + query + "\n")
        writefile.close()
    return render_template('search.html', docs_list=docs_list, value=query, length=len(docs_list))


@app.route("/wildcard_search/<query>&<is_login>&<username>", methods=['POST', 'GET'])
def wildcard_search(query, is_login, username):
    if request.method == 'POST' and request.form.get('cache'):
        cache_value = request.form['cache']
        id_str = cache_value[2:]
        return redirect(url_for('cache', id_str=id_str))
    sorted_result = my_query.wildcard_search(query)
    docs_id = []
    docs_list = []
    for it in sorted_result:
        docs_id.append(it[0])
    for i in docs_id:
        docs_list.append(my_index.doc_list[int(i)])
    if is_login and (username is not None):
        writefile = open("SearchLog/" + username + ".log", 'a', encoding='UTF-8')
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        writefile.write("[" + time + "] " + "search_mode:wildcard_search " + username + " " + query + "\n")
        writefile.close()
    return render_template('search.html', docs_list=docs_list, value=query, length=len(docs_list))


@app.route("/cache/<id_str>", methods=['POST', 'GET'])
def cache(id_str):
    # 先清空之前的临时cache文档
    filename_list = os.listdir("templates")
    for del_name in filename_list:
        if del_name.find("tmp") != -1:
            del_path = os.path.join("templates", del_name)
            os.remove(del_path)
    # 提取快照
    dir = "WebCache"
    html_load_path = "not_found.html" # 快照找不到时的默认路径
    path_list = os.listdir(dir)
    for path in path_list:
        sub_dir = os.path.join(dir, path)
        if os.path.isdir(sub_dir):
            file_list = os.listdir(sub_dir)
            for file_name in file_list:
                name = file_name.split('.')
                name_str = name[0]
                if name_str == id_str:
                    cache_origin_path = os.path.join(sub_dir, file_name)
                    dest_path = os.path.join("templates", "tmp_" + file_name)
                    os.system('copy ' + cache_origin_path + ' ' + dest_path)
                    html_load_path = "tmp_" + file_name
    return render_template(html_load_path)

@app.route("/login/<username>&<password>", methods=['POST', 'GET'])
def login(username, password):
    """
    账号登录，注册账号的步骤就简单化处理不用数据库了，因为只需要用户名和密码，
    这部分也和作业内容关系不大，用户名存在检查密码，不存在注册新用户
    :param username: 用户名
    :param password: 密码
    :return: 初始页面或登录后页面
    """
    filedir_path = "Login/"
    username_list = os.listdir(filedir_path)
    if username in username_list:
        with open(filedir_path + username, 'r', encoding='utf-8') as user_file:
            line = user_file.readline()
            name, pwd = line.split("\t")
            if pwd == password:
                # 密码正确
                return redirect(url_for('logined_index', username=username))
    else:
        writefile = open("Login/" + username, 'w', encoding='UTF-8')
        writefile.write(username + "\t" + password)
        writefile.close()
    return redirect(url_for('index'))


@app.route("/logined_index/<username>", methods=['POST', 'GET'])
def logined_index(username):
    if request.method == 'POST' and request.form.get('login_query'):
        query = request.form['login_query']
        return redirect(url_for('search', query=query, is_login=True, username=username))
    elif request.method == 'POST' and request.form.get('login_phrase_query'):
        query = request.form['login_phrase_query']
        return redirect(url_for('phrase_search', query=query, is_login=True, username=username))
    elif request.method == 'POST' and request.form.get('login_wildcard_query'):
        query = request.form['login_wildcard_query']
        return redirect(url_for('wildcard_search', query=query, is_login=True, username=username))

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
