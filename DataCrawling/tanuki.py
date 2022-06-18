from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver_path = r"chromedriver.exe"

keyword_files = '일본어신조어목록.txt'
with open(keyword_files,'r',encoding='utf-8') as k_f:
    keywords = k_f.readlines()

keywords = [keyword.replace('\n','') for keyword in keywords]

print(keywords)

o = Options()
# o.add_argument('--headless')

d = webdriver.Chrome(driver_path,options=o)

d.get('https://b.2ch2.net/test/search.cgi?t=b&bbs=zatsudan&guid=on')

for keyword in keywords:
    text_file = f'rawdata/{keyword}_tanuki.txt'

    # input_box = d.find_element(By.CSS_SELECTOR, 'input.search_box')
    input_box = d.find_element(By.CSS_SELECTOR, 'body > div: nth - child(6) > form > input.inp')
    input_box.clear()
    input_box.send_keys(keyword)

    # search_button = d.find_element(By.CSS_SELECTOR, 'body > div:nth-child(14) > font > form > input.btn')
    search_button = d.find_element(By.CSS_SELECTOR, 'body > div: nth - child(6) > form > input.fa')
    search_button.click()

    d.implicitly_wait(5)

    # detail_button = d.find_element(By.CSS_SELECTOR, 'body > font > div:nth-child(2) > a:nth-child(2)')
    # detail_button.click()
    #
    # d.implicitly_wait(5)

    texts = []
    i = 1
    while len(texts) < 5000:
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
                    f.writelines(full_text+'\n')
            i += 1

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

    # home = d.find_element(By.CSS_SELECTOR, 'body > div:nth-child(4) > font > a:nth-child(1)')
    # home.click()
    # d.implicitly_wait(5)

d.quit()