import requests
import re
import os
import time
import numpy as np

session = requests.Session()

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0",
           "Referer": "https://dblp.org/search?q=NDSS", "Connection": "close",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "close"}
cookies = {"dblp-search-mode": "c", "dblp-dismiss-new-feature-2019-08-19": "3"}

def get_all_bibtex(url):
    bibtexs = []
    try:
        res = session.get(url, headers=headers, cookies=cookies,verify=False)
    except:
        res = session.get(url, headers=headers, cookies=cookies,verify=False)

    data = str(res.content)
    assert res.status_code == 200
    bibtex_urls = re.compile(\
        r'https://dblp.org/rec/conf/[a-zA-Z0-9]{1,10}/[a-zA-Z0-9]{1,30}.html\?view=bibtex').findall(data)
    # print(bibtex_urls)     # print(len(bibtex_urls))     bibtex_urls = list(set(bibtex_urls))
    for l in bibtex_urls:
        bibtex = get_one_bibtex(l)
        bibtex.replace('\\n','\n')
        bibtexs.append(bibtex)
        time.sleep(abs(np.random.randn()))
        print("[+] get one succ! {}/{}".format(len(bibtexs),len(bibtex_urls)))
    bibtexs = list(set(bibtexs))
    return bibtexs


def get_one_bibtex(url):
    try:
        res = session.get(url, headers=headers, cookies=cookies,verify=False)
    except:
        res = session.get(url, headers=headers, cookies=cookies,verify=False)

    data = str(res.content)

    assert res.status_code == 200
    try:
        bibtex = re.compile(r'@[in]*proceedings{.*}', re.S).findall(data)[0]
        # print(bibtex)         
        return bibtex
    except Exception as e:
        print(e)
        print(data)
    return '{}:error!'.format(url)

def check_exist(output):
    file_path = 'bibtex/{}'.format(output)
    if os.path.exists(file_path):
        return True
    return False