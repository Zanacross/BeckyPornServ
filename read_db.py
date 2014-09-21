__author__ = 'Zanacross'


import sqlite3,os

sql = sqlite3.connect('test.db')
cur = sql.cursor()
with sql:
    cur.execute("SELECT * FROM PornLinks")
    rows = cur.fetchall()

for row in rows:
    print row[0], row[1], row[2]