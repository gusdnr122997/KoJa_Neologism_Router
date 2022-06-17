import win32com.client as win32
import os
import sqlite3

excel = win32.gencache.EnsureDispatch("Excel.Application")

file_path = 'data/신조어_진행상황.xlsx'
full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),file_path)

w = excel.Workbooks.Open(full_path)
s = w.Sheets(4)

korean_data_num = 258
range = f"B4:E{korean_data_num}"
k_data = s.Range(range).Value

japanese_data_num = 156
range = f"H4:K{japanese_data_num}"
j_data = s.Range(range).Value
excel.Quit()

conn = sqlite3.connect('db.sqlite',isolation_level=None)
c = conn.cursor()

k_data = tuple([(x[1],x[2],x[3],1) for x in k_data])
j_data = tuple([x[1],x[3],x[2],2] for x in j_data)
for data in k_data:
    c.execute("SELECT word FROM dictionary WHERE word='%s'" % data[0])
    word = c.fetchone()
    if word is None:
        c.execute("INSERT INTO dictionary(word, meaning, meaning_jp, language_code) VALUES(?, ?, ?, ?)", data)

for data in j_data:
    c.execute("SELECT word FROM dictionary WHERE word='%s'" % data[0])
    word = c.fetchone()
    if word is None:
        c.execute("INSERT INTO dictionary(word, meaning, meaning_jp, language_code) VALUES(?, ?, ?, ?)", data)

conn.close()