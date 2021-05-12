# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 15:23 
# @Author  : Yong Cao
# @Email   : yongcao@fuzhi.ai
# -*- coding: utf-8 -*-
# @Time    : 2021/5/3 9:18 PM
# @Author  : Yong Cao
# @Email   : yongcao@fuzhi.ai
import pickle
import requests
import random
import requests
import re
import os
from urllib.request import urlopen
from tqdm import tqdm
import threading
import math


def get_proxy_list(file_name):
    proxy_list = []
    # ip文件可以浏览我上文链接文章“多线程爬虫——抓取代理ip”
    f = open(file_name)
    # 从文件中读取的line会有回车，要把\n去掉
    line = f.readline().strip('\n')
    while line:
        proxy_list.append(line)
        line = f.readline().strip('\n')
    f.close()
    return proxy_list

def GetUserAgent():
    '''
    功能：随机获取HTTP_User_Agent
    '''
    user_agents=[
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    return user_agents


class Download_Paper_Thread(threading.Thread):
    def __init__(self, threadID, paper_title, paper_url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.paper_title = paper_title
        self.paper_url = paper_url

    def run(self):
        print("开始线程：" + self.name)
        download_paper(self.paper_title, self.paper_url)
        print("退出线程：" + self.name)


def replace(x, old) -> str:
    '''批量替换字符串内容
    :param x: 原始字符串
    :param old: 要替换的内容，`list`
    '''
    for item in old:
        x = x.replace(item, "")
    x = x.strip()
    return x


def download_paper(paper_title, paper_url):
    for i, paper_name in enumerate(paper_title):
        dst_file_name = os.path.join(dst_dir, paper_name+'.pdf')
        dst_file_name = replace(dst_file_name, ['@', '!', '?', '。', '：', ':', '<', '>'])
        print("pdf name: ", dst_file_name)
        if os.path.exists(dst_file_name):
            continue
        response = urlopen(paper_url[i])
        print(paper_url[i], paper_name)
        try:
            file = response.read()
            with open(dst_file_name, 'wb') as f:
                f.write(file)
        except:
            print("unknown name! parser error", paper_name)
            error_file_name.append(paper_name)


if __name__ == '__main__':
    # 配置爬虫
    user_agents = GetUserAgent()
    count = 0
    urls = ["https://www.aclweb.org/anthology/events/acl-2020/#2020-acl-main"]
    url_ins = random.choice(urls)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cookie": "l=AurqcPuigwQdnQv7WvAfCoR1OlrRQW7h; isg=BHp6mNB79CHqYXpVEiRteXyyyKNcg8YEwjgLqoRvCI3ddxqxbLtOFUBGwwOrZ3ad; thw=cn; cna=VsJQERAypn0CATrXFEIahcz8; t=0eed37629fe7ef5ec0b8ecb6cd3a3577; tracknick=tb830309_22; _cc_=UtASsssmfA%3D%3D; tg=0; ubn=p; ucn=unzbyun; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=981798063989731689; hng=CN%7Czh-CN%7CCNY%7C156; um=0712F33290AB8A6D01951C8161A2DF2CDC7C5278664EE3E02F8F6195B27229B88A7470FD7B89F7FACD43AD3E795C914CC2A8BEB1FA88729A3A74257D8EE4FBBC; enc=1UeyOeN0l7Fkx0yPu7l6BuiPkT%2BdSxE0EqUM26jcSMdi1LtYaZbjQCMj5dKU3P0qfGwJn8QqYXc6oJugH%2FhFRA%3D%3D; ali_ab=58.215.20.66.1516409089271.6; mt=ci%3D-1_1; cookie2=104f8fc9c13eb24c296768a50cabdd6e; _tb_token_=ee7e1e1e7dbe7; v=0",
        "User-Agent": random.choice(user_agents)
    }
    # 请求url
    ip_pool = get_proxy_list("ip.txt")
    ip = random.choice(ip_pool)
    proxy = {'http': ip}
    response = requests.get(url_ins, headers=headers, proxies=proxy).text
    # 匹配论文名称和连接
    paper_url = re.findall(r'href=https://www.aclweb.org/anthology/2020.acl-main.(.*?).pdf data-toggle', response)
    paper_url = ["https://www.aclweb.org/anthology/2020.acl-main."+item+".pdf" for item in paper_url]
    paper_title = re.findall(r'href=/anthology/2020.acl-main.*?/>.*?(.*?)</a>', response)
    paper_title = [item.replace("<span class=acl-fixed-case>", "").replace("</span>", "") for item in  paper_title]
    # 下载论文
    dst_dir = "./paper"
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    # 文件存储
    error_file_name = []
    for i, paper_name in enumerate(paper_title):
        paper_name = replace(paper_name, ['@', '!', '?', '。', '：', ':','/','\\','∘', '<', '>'])
        dst_file_name = os.path.join(dst_dir, paper_name+'.pdf')
        if os.path.exists(dst_file_name):
            continue
        response = urlopen(paper_url[i])
        print(paper_url[i], dst_file_name)
        try:
            file = response.read()
            with open(dst_file_name, 'wb') as f:
                f.write(file)
        except Exception as e:
            print(e)
            print("unknown name! parser error", dst_file_name)
            error_file_name.append(dst_file_name)
    print("----------------------------------")
    for item in error_file_name:
        print(item)

    # 想要提速，也可以考虑使用多线程
    # threads_num = 4
    # batch_size = math.ceil(len(paper_url) / 4)
    #
    # threads_list = []
    # for index in range(threads_num):
    #     if index < threads_num - 1:
    #         new_thread = Download_Paper_Thread(index, paper_title[index * batch_size:(index + 1) * batch_size], paper_url[index * batch_size:(index + 1) * batch_size])
    #     else:
    #         new_thread = Download_Paper_Thread(index, paper_title[index * batch_size:], paper_url[index * batch_size:])
    #     # 开启新线程
    #     threads_list.append(new_thread)
    #
    # for thread in threads_list:
    #     thread.start()
    #
    # for thread in threads_list:
    #     thread.join()
    #
    # print("------------------------------------")
    # for item in error_file_name:
    #     print(item)