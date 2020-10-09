import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

sql = 'DELETE FROM myApp_Countries'
cur = con.cursor()
cur.execute(sql)

with open('countries.csv', 'r') as f:
    b = csv.reader(f)
    header = next(b)
    sql = 'insert into myApp_Countries (id, GID_0, NAME_0, GID_1, NAME_1, GID_2, NAME_2, GID_3, NAME_3, AEZ_id) VALUES(?,?,?,?,?,?,?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)

con.commit()
con.close()
