#!/usr/bin/python
# -*- coding: utf-8 -*-


# from urllib import request
import csv
import requests
from bs4 import BeautifulSoup


class FetchData:
    """
    练习国际航空运输协会航空公司代码
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
        target = "https://zh.wikipedia.org/wiki/%E5%9C%8B%E9%9A%9B%E8%88%AA%E7%A9%BA%E9%81%8B%E8%BC%B8%E5%8D%94%E6%9C%83%E8%88%AA%E7%A9%BA%E5%85%AC%E5%8F%B8%E4%BB%A3%E7%A2%BC"
        # 本地保存的路径
        save_path = "G:/爬虫练习/spider_data/country_air_plane_code"

        # 想要爬取网站的根路径
        index_path = "https://zh.wikipedia.org/wiki/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        proxies = {
            'http': "socks5://127.0.0.1:1080",
            'https': "socks5://127.0.0.1:1080"
        }
        req = requests.get(target, headers=headers, proxies=proxies, verify=False)
        # html = request.urlopen(target).read()
        # 查看request默认的编码，发现与网站response不符，改为网站使用的gbk
        req.encoding = 'utf8'

        # 解析HTML
        soup_object = BeautifulSoup(req.text, "html.parser")
        # soup_object = BeautifulSoup(html, "html.parser")
        list_table = soup_object.findAll('table', class_='wikitable')

        csv_all_list = []
        for out_side in list_table:
            # 循环获取每一个章节，获取章节名称，与章节对应的网址
            for row in out_side.findAll("tr"):
                csv_single_list = []
                columns = row.findAll('td')
                # 将当前章节，写入以章节名字命名的txt文件
                if columns:
                    for column in columns:
                        print(column.text)
                        temp_string = column.text.replace('\n', '')
                        temp_string = temp_string.replace('\xa0', '')
                        csv_single_list.append(str(temp_string))
                    csv_all_list.append(csv_single_list)

        print(csv_all_list)
        with open(save_path + '/' + '国际航空运输协会航空公司代码.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['代码', '航空公司', '所属国家或地区'])
            writer.writerows(csv_all_list)


if __name__ == '__main__':
    FetchData.fetch_data()
