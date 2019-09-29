import sqlite3
import csv

con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

#create_table = '''create table fct6 (FCT_id, food_grp_id, food_item_id,Food_grp,Food_name,
#    Crop_ref,Edible,Energy,WATER,Protein,Fat,Carbohydrate,Fiber,ASH,CA,FE,MG,P,K,NA,ZN,CU,
#    VITA_RAE,RETOL,B_Cart_eq,VITD,VITE,THIA,RIBF,NIA,VITB6C,FOL,VITB12,VITC)'''

#create_table = '''create table myapp_FCT (FCT_id int, food_grp_id int, food_item_id int,Food_grp varchar(200),Food_name varchar(200),
#    Crop_ref varchar(200),Edible real,Energy real,WATER real,Protein real,Fat real,Carbohydrate real,Fiber real,ASH real,CA real,FE real,MG real,P real,K real,NA real,ZN real,CU real,
#    VITA_RAE real,RETOL real,B_Cart_eq real,VITD real,VITE real,THIA real,RIBF real,NIA real,VITB6C real,FOL real,VITB12 real,VITC real)'''
#cursor.execute(create_table)

with open('fct.csv', 'r') as f:
    b = csv.reader(f)
    print(b)
    header = next(b)
    sql = 'insert into myApp_FCT (FCT_id, food_grp_id, food_item_id,Food_grp,Food_name,Crop_ref,Edible,Energy,WATER,Protein,Fat,Carbohydrate,Fiber,ASH,CA,FE,MG,P,K,NA,ZN,CU,VITA_RAE,RETOL,B_Cart_eq,VITD,VITE,THIA,RIBF,NIA,VITB6C,FOL,VITB12,VITC) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    for t in b:
        data = t
#        print(t)
        cursor.execute(sql, data)
#        print('go next')
#        cursor.execute('INSERT INTO checkdiet_fct("FCT_id","food_grp_id","food_item_id","Food_grp","Food_name","Crop_ref","Edible","Energy","WATER","Protein","Fat","Carbohydrate","Fiber","ASH","CA","FE","MG","P","K","NA","ZN","CU","VITA_RAE","RETOL","B_Cart_eq","VITD","VITE","THIA","RIBF","NIA","VITB6C","FOL","VITB12","VITC") VALUES (t)')

con.commit()
con.close()
