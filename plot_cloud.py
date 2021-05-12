# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 11:00 
# @Author  : Yong Cao
# @Email   : yongcao@fuzhi.ai
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# import random, requests, re
from ACL_2020_download import replace
import nltk
from nltk.corpus import stopwords
import numpy as np
from PIL import Image


def cloud_generate(words, mask):
    wordcloud = WordCloud(background_color="white",
                          min_font_size=1,
                          max_words=70,
                          collocations=False,
                          mask=mask,
                          width=1600, height=800)
    wordcloud.generate(words)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("img.png", dpi=100)
    plt.show()


if __name__ == '__main__':
    # # 配置爬虫
    # user_agents = GetUserAgent()
    # count = 0
    # urls = ["https://www.aclweb.org/anthology/events/acl-2020/#2020-acl-main"]
    # url_ins = random.choice(urls)
    # headers = {
    #     "Accept": "*/*",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    #     "Cookie": "l=AurqcPuigwQdnQv7WvAfCoR1OlrRQW7h; isg=BHp6mNB79CHqYXpVEiRteXyyyKNcg8YEwjgLqoRvCI3ddxqxbLtOFUBGwwOrZ3ad; thw=cn; cna=VsJQERAypn0CATrXFEIahcz8; t=0eed37629fe7ef5ec0b8ecb6cd3a3577; tracknick=tb830309_22; _cc_=UtASsssmfA%3D%3D; tg=0; ubn=p; ucn=unzbyun; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; miid=981798063989731689; hng=CN%7Czh-CN%7CCNY%7C156; um=0712F33290AB8A6D01951C8161A2DF2CDC7C5278664EE3E02F8F6195B27229B88A7470FD7B89F7FACD43AD3E795C914CC2A8BEB1FA88729A3A74257D8EE4FBBC; enc=1UeyOeN0l7Fkx0yPu7l6BuiPkT%2BdSxE0EqUM26jcSMdi1LtYaZbjQCMj5dKU3P0qfGwJn8QqYXc6oJugH%2FhFRA%3D%3D; ali_ab=58.215.20.66.1516409089271.6; mt=ci%3D-1_1; cookie2=104f8fc9c13eb24c296768a50cabdd6e; _tb_token_=ee7e1e1e7dbe7; v=0",
    #     "User-Agent": random.choice(user_agents)
    # }
    # # 请求url
    # ip_pool = get_proxy_list("ip.txt")
    # ip = random.choice(ip_pool)
    # proxy = {'http': ip}
    # response = requests.get(url_ins, headers=headers, proxies=proxy).text
    # # 匹配论文名称和连接
    # paper_title = re.findall(r'href=/anthology/2020.acl-main.*?/>.*?(.*?)</a>', response)
    # paper_title = [item.replace("<span class=acl-fixed-case>", "").replace("</span>", "") for item in  paper_title]
    # paper_title = " ".join(paper_title)

    # np.save("paper_title.npy", paper_title)
    data = str(np.load("paper_title.npy"))
    print(data)
    data_cut = nltk.word_tokenize(data)

    words = stopwords.words('english')
    filtered_words = [word for word in data_cut if word not in stopwords.words('english')]
    print(filtered_words)
    filtered_words = ' '.join(filtered_words)
    filtered_words = replace(filtered_words, ['dataset', 'Model', "Language", "Neural", "Learning"])
    mask = np.array(Image.open("./123.jpg"))
    cloud_generate(filtered_words, mask)