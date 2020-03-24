import sqlite3
import csv
import random

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('subnational_list.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)

    for t in b:
        data = t

        i = random.randint(1, 100)
        if i < 30:
            res = "ETH-A1"
        elif 30 <= i < 34:
            res = "ETH-SA1"
        elif 34 <= i < 46:
            res = "ETH-SM1"
        elif 46 <= i < 54:
            res = "ETH-SM2"
        elif 54 <= i < 68:
            res = "ETH-M1"
        elif 68 <= i < 80:
            res = "ETH-M2"
        elif 80 <= i < 88:
            res = "ETH-SH1"
        elif 88 <= i < 96:
            res = "ETH-SH2"
        else:
            res = "ETH-H2"

        sql = ('insert into myApp_Countries(GID_0, NAME_0, GID_1, NAME_1, GID_2, NAME_2, GID_3, NAME_3, AEZ_id'
               ') VALUES(?, ?, ?, ?, ?, ?, ?, ?, res)')

        cursor.execute(sql, data)


con.commit()
con.close()
