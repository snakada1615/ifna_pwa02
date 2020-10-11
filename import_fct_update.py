import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

sql = 'DELETE FROM myApp_FCT'
cur = con.cursor()
cur.execute(sql)

with open('fct2.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_FCT (FCT_id, food_grp_id, food_item_id,Food_grp,Food_name,Crop_ref,Edible,Energy,WATER,Protein,Fat,Carbohydrate,Fiber,ASH,CA,FE,MG,P,K,NA,ZN,CU,VITA_RAE,RETOL,B_Cart_eq,VITD,VITE,THIA,RIBF,NIA,VITB6C,FOL,VITB12,VITC,portion_size_init, Food_grp_unicef) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,30,?)'
    for t in b:
        data = t
        cursor.execute(sql, data)

con.commit()
con.close()
