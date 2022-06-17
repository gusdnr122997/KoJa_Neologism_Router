

with open('kowords.txt','r',encoding='utf-8') as wf:
    words = wf.readlines()

words = [w.replace('\n','') for w in words]

# DATA FORMAT = '단어,0,0,우선순위,품사,태그,종성유무,읽기,타입,첫번쨰품사,마지막품사,원형,인덱스표현\n'
data_format = '단어,,,,NNP,*,F,단어,*,*,*,*,*\n'

datas = [data_format.replace('단어',w) for w in words]

with open('kopersons.txt','r',encoding='utf-8') as pf:
    persons = pf.readlines()

persons = [p.replace('\n','') for p in persons]

p_data_format = '사람,,,,NNP,인명,F,사람,*,*,*,*,*\n'
p_datas = [p_data_format.replace('사람',p) for p in persons]