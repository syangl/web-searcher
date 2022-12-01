from time import sleep
from selenium import webdriver
import re
# driver = webdriver.Edge()
#
# driver.get(r'https://www.baidu.com/')
#
# sleep(5)
# driver.close()

# reg1 = r'(//zsb.nankai.edu.cn/gaikuo/.*a)'#贪婪，遇到最后一个a才结束
# # nku_urls网址
# webdata = ['''//zsb.nankai.edu.cn/gaikuo/aaa"
# //zsb.nankai.edu.cn/gaikuo/aaaa
# //zsb.nankai.edu.cn/gaikuo/c'''
#     ,"//zsb.nankai.edu.cn/gaikuo/aaa//zsb.nankai.edu.cn/gaikuo/aaaa//zsb.nankai.edu.cn/gaikuo/c"]
# for i in range(len(webdata)):
#     nku_urls = re.findall(reg1, webdata[i])
#     print(nku_urls)
#
# reg2 = r'(//zsb.nankai.edu.cn/gaikuo/.*?a)'#非贪婪，遇到第一个a就结束
# # nku_urls网址
# webdata = ['''//zsb.nankai.edu.cn/gaikuo/aaa"
# //zsb.nankai.edu.cn/gaikuo/aaaa
# //zsb.nankai.edu.cn/gaikuo/c'''
#     ,"//zsb.nankai.edu.cn/gaikuo/aaa//zsb.nankai.edu.cn/gaikuo/aaaa//zsb.nankai.edu.cn/gaikuo/c"]
# for i in range(len(webdata)):
#     nku_urls = re.findall(reg2, webdata[i])
#     print(nku_urls)

# encoding=utf-8
# 导入爬虫包
from selenium import webdriver
# 睡眠时间
import time
import re
import os
import requests


# 打开编码方式utf-8打开

# 睡眠时间 传入int为休息时间，页面加载和网速的原因 需要给网页加载页面元素的时间
def s(int):
    time.sleep(int)


# html/body/div[1]/table/tbody/tr[2]/td[1]/input
# http://dmfy.emindsoft.com.cn/common/toDoubleexamp.do

if __name__ == '__main__':
    # 查询的文件位置
    # fR = open('D:\\test.txt','r',encoding = 'utf-8')

    # 模拟浏览器，使用谷歌浏览器，将chromedriver.exe复制到谷歌浏览器的文件夹内
    browser = webdriver.Edge()
    # 最大化窗口 用不用都行
    browser.maximize_window()
    #  header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    # 要爬取的网页
    neirongs = []  # 网页内容
    response = []  # 网页数据
    travel_urls = []
    urls = []
    titles = []
    writefile = open("docs.txt", 'w', encoding='UTF-8')
    url = 'http://travel.yunnan.cn/yjgl/index.shtml'
    # 第一页
    browser.get(url)
    response.append(browser.page_source)
    # 休息时间
    s(3)

    # 第二页的网页数据
    # browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
    # s(3)
    # response.append(browser.page_source)
    # s(3)

    # 第三页的网页数据
    # browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
    # s(3)
    # response.append(browser.page_source)

    # 3.用正则表达式来删选数据
    reg = r'href="(//travel.yunnan.cn/system.*?)"'
    # 从数据里爬取data。。。
    # 。travel_urls 旅游信息网址
    for i in range(len(response)):
        travel_urls = re.findall(reg, response[i])

    # 打印出来放在一个列表里
    for i in range(len(travel_urls)):
        url1 = 'http:' + travel_urls[i]
        urls.append(url1)
        browser.get(url1)
        content = browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[3]').text
        # 获取标题作为文件名
        b = browser.page_source
        travel_name = browser.find_element_by_xpath('//*[@id="layer213"]').text
        titles.append(travel_name)
    print(titles)
    print(urls)
    for j in range(len(titles)):
        writefile.write(str(j) + '\t\t' + titles[j] + '\t\t' + str(urls[j]) + '\n')

    s(3)
    browser.close()