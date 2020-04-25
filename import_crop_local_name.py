import sqlite3
import csv
import random

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('crop_local_name.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = ('insert into myApp_Crop_Name(myFCT_id, myCountry_id, Food_grp, Food_name) VALUES(?, ?, ?, ?)')

    for t in b:
        data = t
#        print(t)
        cursor.execute(sql, data)


con.commit()
con.close()
