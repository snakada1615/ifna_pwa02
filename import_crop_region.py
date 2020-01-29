import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

with open('Crop_Region.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_Crop_Region (country,GID_1,FCT_id,food_grp_id,food_item_id,Food_grp,Food_name,suitable_class,Hrv_strt,Hrv_end) VALUES(?,?,?,?,?,?,?,?,?,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)
con.commit()
con.close()
