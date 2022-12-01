# encoding=utf-8
from selenium import webdriver
from time import sleep
import re
import requests

if __name__ == '__main__':
    driver = webdriver.Edge()
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
        sleep(2)

    #删除 404 url
    for i in range(len(old_urls)):
        juge = requests.get(old_urls[i])
        if str(juge) != '<Response [404]>':
            new_urls.append(old_urls[i])

    # 爬取数据
    for count in range(len(new_urls)):
        sleep(2)
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
        print(str(count) + " " +doc_name +"\n")
        writefile = open("../dataset/" + doc_name, 'w', encoding='UTF-8')
        writefile.write(str(count) + '\t' + titles[count] + '\t' + str(new_urls[count]) + '\n' + contents[count] + '\n')

    sleep(2)
    driver.quit()