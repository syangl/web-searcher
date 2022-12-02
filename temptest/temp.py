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

