import kill # KILL ALL CHROMES

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import os, datetime

import bs4_crawling as B

PRINT_LOG = True

def system_log(msg,end="\n"):
    global PRINT_LOG
    if PRINT_LOG:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}",end=end)


keyword_files = '신조어목록.txt'
with open(keyword_files,'r',encoding='utf-8') as k_f:
    keywords = k_f.readlines()

keywords = [keyword.replace('\n','') for keyword in keywords]

def crawl(keywords):
    # https://chromedriver.chromium.org/downloads Chrome-driver download site
    driver_path = r"chromedriver.exe"

    o = Options()
    # Run Background
    o.add_argument('--headless')

    d = webdriver.Chrome(driver_path, options=o)

    d.get('https://search.dcinside.com/combine')

    system_log('DC Crawler Started')
    for I,keyword in enumerate(keywords):
        system_log(f'Currently Doing: {keyword}')
        text_file = f'rawdata/{keyword}_DC.txt'

        input_box = d.find_element(By.CSS_SELECTOR, '#gn_top_search_0')
        input_box.clear()
        input_box.send_keys(keyword)

        search_button = d.find_element(By.CSS_SELECTOR, '#searchform > fieldset > div.top_search.clear > button.sp_img.bnt_search.btn_globalSearch')
        search_button.click()

        d.implicitly_wait(5)

        if I == 0:
            more_tables_button = d.find_element(By.CSS_SELECTOR,'#container > div > section.center_content > div.inner > div.integrate_cont.sch_result > a')
            more_tables_button.click()

            d.implicitly_wait(5)

        details_button = d.find_element(By.CSS_SELECTOR,'#container > div > section.center_content > div.inner > div.integrate_cont.sch_result.result_all > div > div > button:nth-child(2)')
        details_button.click()
        d.implicitly_wait(5)

        links = []
        texts = []

        i = 2
        pg_cnt = 1
        while len(links) + len(texts) < 1500:
            system_log(f'Doing {keyword} Page {pg_cnt} : Total Found',end=" ")
            tables = d.find_elements(By.CSS_SELECTOR,'#container > div > section.center_content > div.inner > div.integrate_cont.sch_result.result_all > ul > li')
            for t in tables:
                a = t.find_element(By.CSS_SELECTOR, 'a')
                p = t.find_element(By.CSS_SELECTOR,'p')
                # title_text = a.text
                p_text = p.text

                if len(p_text) < 20:
                    continue

                if p_text[-3:] != '...':
                    texts.append(p_text)
                    with open(text_file, 'a', encoding='utf-8') as f:
                        f.writelines(p_text+'\n')
                else:
                    href = a.get_attribute('href')
                    status, link_text = B.get_text(href,'DC')
                    if link_text is not None:
                        texts.append(link_text)
                    else:
                        links.append(href)
            print(len(links),len(texts))
            try:
                pg_cnt += 1
                if i > 10:
                    next_page = d.find_element(By.CSS_SELECTOR,'#dgn_btn_paging > a.sp_pagingicon.page_next')
                    i = 4
                else:
                    next_page = d.find_element(By.CSS_SELECTOR,f'#dgn_btn_paging > a:nth-child({i})')
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
    # B.get_text(keywords,'DC')