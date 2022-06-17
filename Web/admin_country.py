import sqlite3

admin = (1,'admin','123','관리자','admin@router.com','9999-99-99','9999-99-99')
country = (
    (1,'한국','한국어'),
    (2,'일본','일본어')
)

conn = sqlite3.connect('db.sqlite',isolation_level=None)
c = conn.cursor()

c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)",admin)
for ct in country:
    c.execute("INSERT INTO countries VALUES(?,?,?)", ct)

conn.close()