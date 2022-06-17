from collections import Counter
import glob

files = glob.glob('rawdata/*.txt')

def check_len(filename):
    with open(filename,'r',encoding='utf-8') as f:
        t = f.readlines()

    c_t = Counter(t)
    lines = 0
    if '--------------------------절단선--------------------------\n' in t:
        lines += c_t['--------------------------절단선--------------------------\n']
    if '------------------------------------!!--------------------------------------\n' in t:
        lines += c_t['------------------------------------!!--------------------------------------\n']

    return lines

for file in files:
    print(file,check_len(file))