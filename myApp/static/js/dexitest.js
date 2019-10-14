var Familydat = {
    db: null,
    db_name: "NFA-db",
    s_name: "Family",
    key_value: "",

    myTbls: {
      'FCT': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']},
      'DRI': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']},
      'DRI_w': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']},
      'Family': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']},
      'Person': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']},
      'Crop': {'key':'pk', 'fields': ['FCT_id', 'food_grp_id', 'food_item_id', 'Food_grp', 'Food_name', 'Crop_ref', 'Edible', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA', 'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']}
    },

    formItem: [
      'name',
      'country',
      'region',
      'province',
      'community',
      'month_start',
      'month_end',
      'remark',
      'protein',
      'vita',
      'fe',
      'size',
      'created_at'
    ],
}


async function init() {
  await new Dexie(Familydat.db_name).open().then(function (db) {
      console.log ("Found database: " + db.name);
      console.log ("Database version: " + db.verno);

  //   ********************************
  //    Activate this part to examine database structure
  //   ********************************
      db.tables.forEach(function (table) {
          console.log ("Found table: " + table.name);
          console.log ("Table Schema: " +
              JSON.stringify(table.schema, null, 4));
      });
      // db table initialize
      //Object.keys(Familydat.myTbls).forEach(function (tbl) {
      //  console.log(tbl + ": '++pk, " + Familydat.myTbls[tbl].fields + "'");
      //});
      Familydat.db = db;

      }).catch('NoSuchDatabaseError', function(e) {
          // Database with that name did not exist
          console.error ("Database not found");
      }).catch(function (e) {
          console.error ("Oh uh: " + e);
      });
}


async function get(s_name, i) {
  if (!Familydat.db) {await init();}

  Familydat.db.table(s_name)
      .get(i)
      .then((rec) => {
          console.log('record:', rec.fields);
          return rec.fields;
      });
}

async function add_web(sname, sid) {
  if (!Familydat.db) {await init();}

  //collect latest post from server and store in idb.
//  await orgDat = fetch('http://127.0.0.1:8000/getNFA/' + sid + '/');


}


async function add_form() {

}

console.log(get('Person',3));
