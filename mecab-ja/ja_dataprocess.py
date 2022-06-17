import glob

DELETE_TAGS = ['助詞','記号']

ja_dir = 'before'

files = glob.glob(ja_dir+'*.txt')
keywords = [x.split('_')[0].split('\\')[-1] for x in files]

texts = []

for f,k in zip(files,keywords):
  with open(f,'r',encoding='utf-8') as txtf:
    texts.append([txtf.readlines(),k])

for i in range(len(texts)):
  texts[i][0] = list(set(texts[i][0]))

import re
import MeCab

result = []

# MeCab dict neologd
tagger = MeCab.Tagger(r'-d "C:\mecab-ipadic-neologd"')

with open('일본어불용어.txt', 'r', encoding='utf-8') as sfile:
    stopwords = sfile.readlines()

stopwords = [x.replace('\n', '') for x in stopwords]

for i in range(len(texts)):
    txts, keyword = texts[i][0], texts[i][1]
    print(keyword,len(txts))
    for t in txts:
        text = t.replace(keyword, '마스크')
        text = text.replace('\n', '')
        text = text.replace(' - dc official App', '')
        text = re.sub('(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', text)
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
        text = re.sub('[a-zA-Z]','',text)
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
            parse = tagger.parse(text).split('\n')
            tokens = [p.split(',') for p in parse]
            new_tokens = []
            for tok in tokens:
                if tok == ['EOS']:
                    break
                c_word,tag = tok[0].split('\t')
                # print(c_word,tag)
                if c_word == '마스크': # 마스크 단어 추가
                    new_tokens.append(c_word)
                elif tag == '助詞' or tag == '記号':  # 조사 or 기호
                    continue
                elif tag == '助動詞':  # 조동사
                    if len(new_tokens) == 0:
                        continue
                    else:
                        v = new_tokens.pop()
                        new_tokens.append(v+c_word)
                elif c_word in stopwords:
                    continue
                else:
                    new_tokens.append(c_word)

            if len(new_tokens) > 10:
                new_text = " ".join(new_tokens).replace('마스크', keyword)
                if new_text not in result:
                    result.append(new_text)
        else:
            pass

texts = result

from tqdm import tqdm
import datetime

with open(f"after/ja{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt", 'w',encoding='utf-8') as out:
  for line in tqdm(texts, unit=' line'):
    out.write(''.join(line) + '\n')
