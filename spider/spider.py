# encoding=utf-8
import gzip
import os
import urllib.request
from io import BytesIO

from selenium import webdriver
from time import sleep
import re
import requests
import random

from other_tools.delete_files import del_files
from other_tools.process_bar import process_bar

CACHE_SIZE = 5
cur_cache_size = 0

filedir_path = "../WebCache/"

if __name__ == '__main__':
    driver = webdriver.Edge(executable_path="D:\\EdgeDriver\\v109.0.1518.70\\msedgedriver.exe")
    driver.maximize_window()

    # 要爬取的网页
    old_urls = []
    new_urls = []
    titles = []
    contents = []  # 网页内容
    origin_url = "http://news.nankai.edu.cn/nkrw"
    # 第一页网页数据,总页数npage
    driver.get(origin_url)
    npage = 62
    # 正则表达式筛数据
    reg = r'href="(http://news.nankai.edu.cn/nkrw/system.*?)"'

    sleep(3)

    for i in range(npage):
        webdata = []  # 网页数据
        webdata.append(driver.page_source)
        # urls网址
        for i in range(len(webdata)):
            old_urls.extend(re.findall(reg, webdata[i]))
        driver.find_element_by_link_text("下一页").click()
        sleep(random.randint(2, 3))

    # 删除 404 url
    old_len = len(old_urls)
    for i in range(old_len):
        # sleep(random.randint(2, 3))
        juge = requests.get(old_urls[i])
        if str(juge) != '<Response [404]>':
            new_urls.append(old_urls[i])
        process_bar(i + 1, old_len)
    print("\n")

    # 创建cache log，获取当前cache大小
    cache_line_list = os.listdir(filedir_path)
    if "cache_size.log" not in cache_line_list:
        with open(filedir_path + "cache_size.log", 'w', encoding='UTF-8') as log_file:
            log_file.write("current_size:" + str(len(cache_line_list)) + "\ncache_size:" + str(CACHE_SIZE) + "\n")
    else:
        with open(filedir_path + "cache_size.log", 'r', encoding='UTF-8') as log_file:
            line = log_file.readline()
            size = line.split(':')
            cur_cache_size = int(size[1])
    # 爬取数据
    for count in range(len(new_urls)):
        sleep(random.randint(2, 3))
        driver.get(new_urls[count])
        # 获取标题 文档名
        story_name = \
            driver.find_element_by_xpath \
                ("/html/body/div/table[3]/tbody/tr/td[1]/table[2]/tbody/tr[1]/td").text
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        story_title = re.sub(rstr, '_', story_name)
        titles.append(story_title)
        # 获取内容 文档内容
        story_content = \
            driver.find_element_by_xpath \
                ("/html/body/div/table[3]/tbody/tr/td[1]/table[2]/tbody/tr[3]/td").text
        contents.append(story_content)
        # 创建txt文档并写入
        doc_name = str(count) + "-" + titles[count] + ".txt"
        print(str(count) + " " + doc_name + "\n")
        writefile = open("../dataset/" + doc_name, 'w', encoding='UTF-8')
        writefile.write(str(count) + '\t' + titles[count] + '\t' + str(new_urls[count]) + '\n' + contents[count] + '\n')
        # 保存网页快照，替换最早保存的网页
        html_bin = urllib.request.urlopen(new_urls[count]).read()
        buf = BytesIO(html_bin)
        f = gzip.GzipFile(fileobj=buf)
        html_str = f.read().decode('utf-8')

        if cur_cache_size < CACHE_SIZE:
            if not os.path.exists(filedir_path + str(cur_cache_size)):
                os.mkdir(filedir_path + str(cur_cache_size))
            with open(filedir_path + str(cur_cache_size) + "/" + str(count) + ".html", 'w', encoding='UTF-8') as html_file:
                html_file.write(html_str)
            cur_cache_size += 1
        else:
            cur_pos = count % CACHE_SIZE
            # 清空旧cache line
            del_files(filedir_path + str(cur_pos))
            with open(filedir_path + str(cur_pos) + "/" + str(count) + ".html", 'w', encoding='UTF-8') as html_file:
                html_file.write(html_str)

    cache_list = os.listdir(filedir_path)
    with open(filedir_path + "cache_size.log", 'w', encoding='UTF-8') as log_file:
        log_file.write("current_size:" + str(len(cache_list) - 1) + "\ncache_size:" + str(CACHE_SIZE) + "\n")

    sleep(2)
    driver.quit()
