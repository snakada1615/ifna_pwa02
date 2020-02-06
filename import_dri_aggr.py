import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('DRI_aggr.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_DRI_aggr (nut_group, protein, vita, fe) VALUES(?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)

con.commit()
con.close()
