#! -*- encoding:utf-8 -*-

import web
import urllib
import urllib2
import time
import random
import sys
import json
import traceback

from multiprocessing import Process, Queue, Pool


reload(sys)
sys.setdefaultencoding('utf-8')

# db = web.database(host='127.0.0.1', port=3306, dbn='mysql', db='fanfan', user='root', pw='mysql')
db = web.database(host='127.0.0.1', port=3306, dbn='mysql', db='fanfan', user='root', pw='Tz09Jk4h%7X')


url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?"

user_agent_list = [
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Version/6.0 Mobile/10A5355d Safari/8536.25',
	'Chrome/28.0.1468.0 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
	]


idcard_header_queue = Queue()


with open(sys.argv[1], 'r') as fr:
    for line in fr:
        idcard_header_queue.put(line.strip())


def main_work(item):
    para={
        'resource_id': 6899,
        'query': '失信被执行人名单',
        'cardNum': item,
        'iname': '',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'format': 'json',
        'pn': 0
    }
    headers = {'User-Agent': user_agent_list[random.randint(0, len(user_agent_list)-1)]}
    NO_OVER = True
    count = 0
    res = []
    while NO_OVER:
        try:
            targetUrl = url + urllib.urlencode(para)
            req = urllib2.Request(targetUrl, headers=headers)
            r = urllib2.urlopen(req, timeout=10).read()
            result = json.loads(r)
            court_record = result['data']
            res.append(court_record)
            if len(court_record) == 0:
                NO_OVER = False
            para['pn'] = para['pn'] + 50
        except:
            pass
    return res


#def save_sql(name, idcard):
#    try:
#        return db.select('brokelist', where='name=$name and idcard=$idcard', vars=locals())[0]
#    except:
#        return db.insert('brokelist', name=name, idcard=idcard, create_time=int(time.time()))


def mycallback(res):
    for item in res:
        if item:
            name = item[0]['result'][0]['iname']
            idcard = item[0]['result'][0]['cardNum']
            with open('brokelist.txt', 'a') as f:
                f.write(name + ',' + idcard + '\n')
            #save_sql(name, idcard)


if __name__ == '__main__':
    pool = Pool(processes=4)
    idcard_header_length = idcard_header_queue.qsize()
    for i in range(idcard_header_length):
        item = idcard_header_queue.get()
        pool.apply_async(main_work, (item,), callback=mycallback)
    pool.close()
    pool.join()

