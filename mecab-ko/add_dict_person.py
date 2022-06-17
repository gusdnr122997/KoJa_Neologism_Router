PERSON_CSV_FILE_PATH = 'C:\\mecab\\user-dic\\person.csv'
P_CSV_FILE_PATH = "C:\\mecab\\mecab-ko-dic\\user-person.csv"

from make_newword_data import p_datas, persons

# ADD FILES
with open(PERSON_CSV_FILE_PATH,'r',encoding='utf-8') as f:
    file_data = f.readlines()

last_index = len(file_data)
file_words = [d.split(',')[0] for d in file_data]

for p,data in zip(persons, p_datas):
    if p not in file_words:
        print('NEW WORD:',p)
        file_data.append(data)

with open(PERSON_CSV_FILE_PATH,'w',encoding='utf-8') as f:
    for line in file_data:
        f.write(line)

# Open Window PowerShell in Administrative And Do Below Commands
# CD C:\mecab
# .\tools\add-userdic-win.ps1

def add_priority():
    with open(PERSON_CSV_FILE_PATH,'r',encoding='utf-8') as f:
        file_data = f.readlines()

    for i in range(len(file_data)):
        temp = file_data[i].split(',')
        print(temp[0],temp[1],temp[2],temp[3])
        if temp[3] == '':
            temp[1] = '1788'
            temp[2] = '3549'
            temp[3] = '0'
        file_data[i] = ",".join(temp)

    with open(P_CSV_FILE_PATH, 'w', encoding='utf-8') as f:
        for line in file_data:
            f.write(line)

    with open(P_CSV_FILE_PATH, 'r', encoding='utf-8') as f:
        file_data = f.readlines()

    return file_data

# CD C:\mecab
# .\tools\compile-win.ps1
