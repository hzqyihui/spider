#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup


class FetchData:
    """
    练习小说爬取
    """
    def __init__(self):
        """
        构造函数
        """
        pass

    @staticmethod
    def fetch_data():
        """
        从小说网站直接获取小说
        :return:
        """
        # 想要爬取的小说主页
        target = "https://www.biqubao.com/book/17570/"
        # 本地保存的路径
        save_path = "E:/爬虫练习/spider_data/small_story"

        # 想要爬取网站的根路径
        index_path = "https://www.biqubao.com"

        req = requests.get(target)
        # 查看request默认的编码，发现与网站response不符，改为网站使用的gbk
        print(req.encoding)
        req.encoding = 'gbk'

        # 解析HTML
        soup_object = BeautifulSoup(req.text, "html.parser")
        list_tag = soup_object.div(id="list")
        # 打印每个章节小说的路径的链接元素
        print('list_tag:', list_tag)

        # 获取小说名称
        story_title = list_tag[0].dl.dt.string
        # 根据小说名称创建一个文件夹，如果不存在就创建
        dir_path = save_path + '/' + story_title
        if not os.path.exists(dir_path):
            os.path.join(save_path, story_title)
            os.mkdir(dir_path)

        i = 0
        # 循环获取每一个章节，获取章节名称，与章节对应的网址
        for ddTag in list_tag[0].dl.find_all('dd'):
            i += 1
            # 章节名称
            chapter_name = ddTag.string
            # 章节网址
            chapter_url = index_path + ddTag.a.get('href')
            # 访问该章节详情网址，爬取该章节正文
            chapter_req = requests.get(url=chapter_url)
            chapter_req.encoding = 'gbk'
            chapter_soup = BeautifulSoup(chapter_req.text, "html.parser")

            # 解析正文所在的标签：
            content_tag = chapter_soup.div.find(id="content")
            # 获取正文文本，并将空格替换为换行符
            content_text = str(content_tag.text.replace('\xa0', '\n'))

            # 将当前章节，写入以章节名字命名的txt文件
            with open(dir_path + '/' + chapter_name + '.txt', 'w') as f:
                f.write('本文网址： ' + chapter_url)
                f.write(content_text)


if __name__ == '__main__':
    FetchData.fetch_data()






