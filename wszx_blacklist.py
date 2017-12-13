# -*- coding: utf-8 -*-

# 使用BeautifulSoup进行的爬虫。提取其中所需要的字段，并把获取到的list分割为更小的list

import random
import urllib2

from bs4 import BeautifulSoup


user_agent_list = [
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
]


headers = {'User-Agent': random.choice(user_agent_list)}


# 拼接URL，返回HTML
def get_url(page):
    url = 'http://www.wszx.cc/hmd2016-index-selected-2-p-' + str(page) + '.html'
    print 'loding -------> NO- %d ' % page
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request, timeout=10).read()
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            print e.code
        if hasattr(e, 'reason'):
            print e.errno
    # 返回时调用提取信息函数
    return get_info(html)


# 从返回的HTML中提取自己需要的信息
def get_info(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    # 提取其中的所有dd标签
    results = soup.find_all('dd')
    # 把获取到的信息list按照4个一组，分割为更小的list
    user_info = [results[i:i+4] for i in range(0, len(results), 4)]
    info_list = []
    for info in user_info:
        idcard = info[0].get_text()
        name = info[1].get_text()
        phone = info[3].get_text()
        info_list.append({'idcard': idcard, 'name': name, 'phone': phone})
    # 调用存储函数
    return save_info(info_list)


# 存储到文本
def save_info(info_list):
    for i in info_list:
        with open('wszx_blacklist.txt', 'a') as f:
            f.write(str(i) + '\n')


if __name__ == '__main__':
    for i in range(1, 78):
        get_url(i)

