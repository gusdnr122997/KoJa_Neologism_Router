from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import requests
from time import sleep
import glob

import random

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

result_status = []
result_text = []


def get_links_keywords():
    return [x.split("links\\")[-1].split('_link')[0] for x in glob.glob('links/*.txt')]


def read_links(txtfile):
    with open(txtfile,'r',encoding='utf-8') as f:
        links = f.readlines()

    return [x.replace('\n','') for x in links]


def parse_url(url):
    url_parsed = urlparse(url)

    new_url = url.replace('?' + url_parsed.query, '')

    return new_url, url_parsed.query


def get_text(keywords,platform='None'):
    for keyword in keywords:
        urls = read_links(f'links/{keyword}_links.txt')
        file_name = f'rawdata/{keyword}_{platform}.txt'
        with open(file_name,'a',encoding='utf-8') as f:
            texts = []
            for url in urls:
                if len(result_status)%11 == 10:
                    sleep(random.randint(1,10))
                new_url,p = parse_url(url)

                res = requests.get(new_url,params=p,headers=headers)
                print(res.status_code)
                print(res.text)
                if res.status_code != 200:
                    continue
                result_status.append(res.status_code)
                result_text.append(res.text)

                soup = BeautifulSoup(res.text,'html.parser')
                if platform == 'DC':
                    selected_text = soup.select_one('div.write_div')
                elif platform == 'PANN':
                    selected_text = soup.select_one('div#contentArea')

                if selected_text is None:
                    pass
                else:
                    texts.append(selected_text.text)
                    f.writelines(selected_text.text+'\n')