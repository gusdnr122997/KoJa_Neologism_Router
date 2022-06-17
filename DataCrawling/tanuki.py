from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

driver_path = r"chromedriver.exe"

o = Options()
o.add_argument('--headless')

d = webdriver.Chrome(driver_path,options=o)

d.get('https://b.2ch2.net/zatsudan/i/')

keyword_files = '일본어_신조어_목록.txt'
with open(keyword_files,'r',encoding='utf-8') as k_f:
    keywords = k_f.readlines()

keywords = [keyword.replace('\n','') for keyword in keywords]

print(keywords)
for keyword in keywords:
    text_file = f'rawdata/{keyword}_tanuki.txt'

    input_box = d.find_element(By.CSS_SELECTOR, 'input.search_box')
    # input_box.clear()
    input_box.send_keys(keyword)

    d.implicitly_wait(5)
    search_button = d.find_element(By.CSS_SELECTOR, 'body > div:nth-child(14) > font > form > input.btn')
    search_button.click()

    d.implicitly_wait(5)

    detail_button = d.find_element(By.CSS_SELECTOR, 'body > font > div > a:nth-child(2)')
    detail_button.click()

    d.implicitly_wait(5)

    # links = []
    texts = []

    i = 1
    while len(texts) < 100:
        before_text_len = len(texts)
        tables = d.find_elements(By.CSS_SELECTOR,'body > font:nth-child(10) > div > div')
        max = len(tables)
        print(max)
        for t in tables:
            a = t.find_element(By.CSS_SELECTOR, f'div:nth-child({i}) > div.res.inner')
            full_text = a.text
            print(full_text)
            if full_text in texts:
                pass
            else:
                texts.append(full_text)
                with open(text_file, 'a', encoding='utf-8') as f:
                    f.writelines(full_text)
                    f.writelines('\n--------------------------절단선--------------------------\n')
            i += 1

            # href = a.get_attribute('href')
            # texts.append(href)
            if i > max:
                try:
                    next_page = d.find_element(By.CSS_SELECTOR, 'body > table:nth-child(11) > tbody > tr > td > font > input[type=button]:nth-child(3)')
                    next_page.click()
                    i = 1
                    d.implicitly_wait(10)
                except:
                    pass
        if before_text_len == len(texts):
            break


    home = d.find_element(By.CSS_SELECTOR, 'body > div:nth-child(4) > font > a:nth-child(1)')
    home.click()
    d.implicitly_wait(5)

    # link_file = f'/Users/kimwooyoung/Documents/project/DataCrawling/links/{keyword}_links(tanuki).txt'
    # if os.path.exists(link_file):
        # os.remove(link_file)
    # print(links)
    # with open(link_file,'a',encoding='utf-8') as f:
    #     for l in links:
    #         f.writelines(l)
    #         f.writelines('\n')

d.quit()

# B.get_text(keywords)