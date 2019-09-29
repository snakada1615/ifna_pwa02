import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('DRI.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_DRI (age_id,male_protain,male_vitA,male_fe,female_protain,female_vitA,female_fe) VALUES(?,?,?,?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)

con.commit()
con.close()
