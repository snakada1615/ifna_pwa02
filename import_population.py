import sqlite3
import csv
import random

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('population.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = ('insert into myApp_pop(NAME_0, GID_0, Year, Age_class, Age_class_id, share_Pop, share_Preg, share_BF'
           ') VALUES(?, ?, ?, ?, ?, ?, ?, ?)')

    for t in b:
        data = t
#        print(t)
        cursor.execute(sql, data)


con.commit()
con.close()
