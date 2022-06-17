from konlpy.tag import Mecab
import re, glob, datetime

COMMERCIAL = ['◐','☎','♨','♬','◆']
DEL_TAGS = ['SF','SE','SS','SSO','SSC','SP','SC','SO','SW','SY','UNKNOWN']

# Mecab for Ko
tagger = Mecab(dicpath='C:\\mecab\\mecab-ko-dic')

ko_dir = "before"

files = glob.glob(ko_dir+'/*.txt')
keywords = [x.split('_')[0].split('\\')[-1] for x in files]

texts = {}

num = 0
for f,k in zip(files,keywords):
  if k not in texts:
    texts[k] = []

  with open(f,'r',encoding='utf-8') as txtf:
    for l in txtf.readlines():
      if l not in texts[k]:
        texts[k].append(l)

result = []

with open('한국어불용어.txt', 'r', encoding='utf-8') as sfile:
    stopwords = sfile.readlines()

stopwords = [x.replace('\n', '') for x in stopwords]

for k, txts in texts.items():
    new_texts = []
    print(k,len(txts))
    for t in txts:
        t = t.replace(k,'搭')  # 신조어 마스킹
        text = t.replace('\n', '')
        text = text.replace(' - dc official App', '')
        text = re.sub('(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', text)
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
        if not re.findall('[a-zA-Z]',k):
            text = re.sub('[a-zA-Z]','',text)
        text = re.sub('ㅋ{1,10}', '', text)
        text = re.sub('ㅎ{1,10}', '', text)
        text = re.sub('ㅠ{1,10}', '', text)
        text = re.sub('ㅜ{1,10}', '', text)
        text = re.sub('w{1,10}', '', text)
        text = re.sub('ｗ{1,10}', '', text)
        text = re.sub('W{1,10}', '', text)
        text = re.sub('[0-9]', '', text)
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        if len(text) > 10:
            tokens = tagger.pos(text)
            new_text = []
            for tok in tokens:
                ko_word, tag = tok
                if tag in DEL_TAGS:
                    continue
                elif tag[0] == 'J': # 조사태그 제거
                    continue
                elif tag == 'ETN' or tag == 'ETM' or tag == 'EP' or tag[:2] == 'XS':# 접미사
                    if len(new_text) == 0:
                        continue
                    else:
                        v = new_text.pop()
                        new_text.append(v+ko_word)
                elif tag == 'EC' or tag == 'EF': # 용언에 붙는 접미사
                    if len(new_text) == 0:
                        continue
                    else:
                        v = new_text.pop()
                        new_text.append(v+'다')
                # elif ko_word in stopwords:
                #     continue
                else:
                    new_text.append(ko_word)

            if len(new_text) > 10:
                text = " ".join(new_text)
                text = text.replace('搭',k)  # 신조어 마스킹 해제
                print(k,text)
                new_texts.append(text)
            else:
                pass

    texts[k] = new_texts

# XLSX 형식으로 저장
import win32com.client as win32

xl = win32.gencache.EnsureDispatch('Excel.Application')
wb = xl.Workbooks.Add()
s1 = wb.Sheets(1)
s1.Name = 'train'

s1.Cells(1,1).Value = '단어'
s1.Cells(1,2).Value = '문장'

i1,i2,i3 = 2,2,2
for k,txts in texts.items():
    print(k)
    for t in txts:
        s1.Cells(i1,1).Value = k
        s1.Cells(i1,2).Value = t
        i1 += 1

file_name = os.path.dirname(__file__)
wb.SaveAs(file_name + f"after\\ko_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
xl.Quit()
