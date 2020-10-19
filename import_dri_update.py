import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

sql = 'DELETE FROM myApp_DRI'
cur = con.cursor()
cur.execute(sql)

with open('dri_new.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_DRI (id, nut_group, energy, protein, vita, fe, max_vol) VALUES(?,?,?,?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)

con.commit()
con.close()
