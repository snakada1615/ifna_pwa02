import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('DRI_women.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_DRI_women (status,female_prot2,female_vit2,female_fe2) VALUES(?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)


con.commit()
con.close()
