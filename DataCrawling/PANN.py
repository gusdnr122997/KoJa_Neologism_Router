from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os

import bs4_crawling as B


keyword_files = '신조어목록.txt'
with open(keyword_files,'r',encoding='utf-8') as k_f:
    keywords = k_f.readlines()

keywords = [keyword.replace('\n','') for keyword in keywords]

def crawl(keywords):
    driver_path = r"chromedriver.exe"

    o = Options()
    o.add_argument('--headless')

    d = webdriver.Chrome(driver_path, options=o)
    d.get('https://pann.nate.com/')

    first_page = True
    for keyword in keywords:
        text_file = f'rawdata/{keyword}_pann.txt'

        input_box = d.find_element(By.CSS_SELECTOR, '#input_search')
        input_box.clear()
        input_box.send_keys(keyword)

        search_button = d.find_element(By.CSS_SELECTOR, '#search > fieldset > button')
        search_button.click()

        d.implicitly_wait(5)

        more_tables_button = d.find_element(By.CSS_SELECTOR,'#container > div.content.sub > div.srcharea > div:nth-child(4) > p > a')
        more_tables_button.click()

        d.implicitly_wait(5)

        links = []
        texts = []

        i = 2
        num = 1
        tries = 0
        while len(links) + len(texts) < 300:
            if tries == 20:
                break
            tables = d.find_elements(By.CSS_SELECTOR,'#container > div.content.sub > div.srcharea > div.srch_list.section > ul > li')
            for t in tables:
                a = t.find_element(By.CSS_SELECTOR, 'div.tit > a')
                p = t.find_element(By.CSS_SELECTOR, 'div.txt > a')
                title_text = a.text
                p_text = p.text
                num += 1

                if keyword not in p_text:
                    if keyword in title_text:
                        if len(title_text) < 10:
                            continue
                        texts.append(title_text)
                        with open(text_file, 'a', encoding='utf-8') as f:
                            f.writelines(title_text+'\n')
                    continue

                if p_text[-3:] != '...':
                    if len(p_text) < 15:
                        continue
                    texts.append(p_text)
                    with open(text_file, 'a', encoding='utf-8') as f:
                        f.writelines(p_text+'\n')
                else:
                    href = a.get_attribute('href')
                    links.append(href)

            try:
                tries += 1
                if first_page:
                    if i > 10:
                        next_page = d.find_element(By.CSS_SELECTOR, '#container > div.content.sub > div.srcharea > div.paginate > a.btn.next')
                        first_page = False
                        i = 3
                    else:
                        next_page = d.find_element(By.CSS_SELECTOR, f'#container > div.content.sub > div.srcharea > div.paginate > a:nth-child({i})')
                        i += 1
                elif i > 11:
                    next_page = d.find_element(By.CSS_SELECTOR,'#container > div.content.sub > div.srcharea > div.paginate > a.btn.next')
                    i = 3
                else:
                    next_page = d.find_element(By.CSS_SELECTOR,f'#container > div.content.sub > div.srcharea > div.paginate > a:nth-child({i})')
                    i += 1
                next_page.click()

            except Exception as err:
                print(err)
                break

        link_file = f'links/{keyword}_links.txt'
        if os.path.exists(link_file):
            os.remove(link_file)

        with open(link_file,'a',encoding='utf-8') as f:
            for l in links:
                f.writelines(l)
                f.writelines('\n')

    d.quit()

if __name__ == '__main__':
    crawl(keywords)
    B.get_text(keywords,'PANN')