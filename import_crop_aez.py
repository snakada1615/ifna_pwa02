import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('Crop_AEZ2.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_Crop_AEZ (myFCT_id,AEZ_id) VALUES(?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)


con.commit()
con.close()
