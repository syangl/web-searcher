# encoding=utf-8
from selenium import webdriver
from time import sleep
import re

if __name__ == '__main__':
    driver = webdriver.Edge()
    driver.maximize_window()

    # 要爬取的网页
    urls = []
    titles = []
    contents = []  # 网页内容
    origin_url = "http://news.nankai.edu.cn/nkrw"
    # 第一页网页数据,总页数npage
    driver.get(origin_url)
    npage = 63
    # 正则表达式筛数据
    reg = r'href="(http://news.nankai.edu.cn/nkrw/system.*?)"'

    sleep(3)

    # 爬取数据
    count = 0
    for i in range(npage):
        webdata = []  # 网页数据
        webdata.append(driver.page_source)
        # urls网址
        for i in range(len(webdata)):
            urls.extend(re.findall(reg, webdata[i]))
        #保存当前窗口句柄
        window_handle = driver.current_window_handle
        # 爬取子链接内容
        for count in range(len(urls)):
            sleep(2)
            driver.get(urls[count])
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
            writefile = open("../dataset/" + doc_name, 'w', encoding='UTF-8')
            writefile.write(str(count) + '\t' + titles[count] + '\t' + str(urls[count]) + '\n' + contents[count] + '\n')
            count += 1
        #返回之前主窗口
        driver.switch_to.window(window_handle)
        driver.find_element_by_link_text("下一页").click()
        sleep(2)

    # print(titles)
    # print(urls)
    # #
    # for j in range(len(titles)):
    #     writefile.write(str(j) + '\t' + titles[j] + '\t' + str(urls[j]) + '\n')

    sleep(2)
    driver.close()