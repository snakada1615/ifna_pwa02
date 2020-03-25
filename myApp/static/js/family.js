var Familydat = {
    db: null,
    db_name: "NFA-db",
    s_name: "Family",
    key_value: "",

    myTbls: {
      'FCT': {
        'key':'pk',
        'fields': ['FCT_id','food_grp_id','food_item_id','Food_grp',
          'Food_name','Crop_ref','Edible','Energy','WATER','Protein',
          'Fat','Carbohydrate','Fiber','ASH','CA','FE','MG','P','K',
          'NA','ZN','CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD',
          'VITE', 'THIA', 'RIBF', 'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC']
        },
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
  // Create your instance
  var db = new Dexie(Familydat.db_name);

  // Define your schema
  db.version(0.1).stores({
    FCT: "++pk",
    DRI: "++pk",
    DRI_w: "++pk",
    Family: "++pk",
    Person: "++pk",
    Crop: "++pk"
  });

  await db.open().then(function (db) {
    console.log ("Found database: " + db.name);
//    console.log ("Database version: " + db.verno);
    Familydat.db = db;

    //// DB読み込みが終わったら画面描画
    if (getHTML_name() == "Family/create") { render_form(5); }
    if (getHTML_name() == "Family/list") {getall("Family");}

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

async function getall(s_name) {
  let records;
  try {
    if (!Familydat.db) {await init();}
    records = await Familydat.db.table(s_name).toArray();
  } catch (err) {
      console.log("getall", err);
      return;
  }
  for (i=0; i<records.length; i++) {
    render_list(records[i]);
  }
}


async function put_web(sname, sid) {
  if (!Familydat.db) {await init();}

  //collect latest post from server and store in idb.
//  await orgDat = fetch('http://127.0.0.1:8000/getNFA/' + sid + '/');


}

function render_form(mykey) {
    for (var i=0; i<Familydat.formItem.length; i++) {
      var d = '';
      d += "<div class='row'>";
      d += "<div class='col-3'>";
      d += "<p>" + Familydat.formItem[i] + "</p>";
      d += "</div>";
      d += "<div class='col-9'>";
      d += "<input id='" + Familydat.formItem[i] + "' type='text' placeholder='put information here' >";
      d += "</div>";
      d += "</div>";

//      if (myKey != "") {
//        var myVal = Familydat.getRecord("Family", myKey);
//        console.log("myDat");
//        console.log(myVal);
//      }

      var div = document.createElement('div');
      div.innerHTML = d;
      document.getElementById("family_form").appendChild(div);
    }
}

function render_list(myDat) {
    var d = '';
    d += "        <div class='card border-primary col-12 mt-2' style='max-width: 540px;'>";
    d += "    		  <div class='row'>";
    d += "    		    <div class='col-4 d-flex align-items-center'>";
    d += "    		      <img src='../../../static/img/152053house192.png' %}" +" class='card-img'>";
    d += "    		    </div>";
    d += "    		    <div class='col-8'>";
    d += "    		      <div class='card-body bg-light p-2'>";
    d += "    		        <h5 class='card-title'>";
    d +=     							myDat.fields.name;
    d += "    						</h5>";
    d += "    						<p class='card-text'>";
    d +=     							myDat.fields.size;
    d += "    						</p>";
    d += "    						<p class='card-text'>";
    d +=     							myDat.fields.remark;
    d += "    						</p>";
    d += "    						<p>";
    d += "    							<span><a class='btn btn-light btn-sm align-middle badge badge-secondary' href='{% url 'Family_update' pk=family.pk %}'>info</a></span>";
    d += "    							<span><a class='btn btn-light btn-sm align-middle badge badge-secondary' href='{% url 'Family_delete' pk=family.pk %}'>del </a></span>";
    d += "    						</p>";
    d += "    						<p>";
    d += "    							<span><a class='btn btn-light btn-sm align-middle badge badge-secondary' href='{% url 'person_list' familyid=family.pk %}'>trgt</a></span>";
    d += "    							<span><a class='btn btn-light btn-sm align-middle badge badge-secondary' href='{% url 'crop_list' familyid=family.pk %}'>crop</a></span>";
    d += "    						</p>";
    d += "    		      </div>";
    d += "    		    </div>";
    d += "    		  </div>";
    d += "    		</div>";

    var div = document.createElement('div');
    div.className = 'container';
    div.innerHTML = d;
    document.getElementById("family_list").appendChild(div);
}


async function put_form() {
  if (!Familydat.db) {await init();}

    var formdat = {}
    var jsondat = {}
    var text = document.getElementById('name').value;
    formdat.name = text;
    var text = document.getElementById('country').value;
    formdat.county = text;
    var text = document.getElementById('region').value;
    formdat.region = text;
    var text = document.getElementById('province').value;
    formdat.province = text;
    var text = document.getElementById('community').value;
    formdat.community = text;
    var text = document.getElementById('month_start').value;
    formdat.month_start = text;
    var text = document.getElementById('month_end').value;
    formdat.month_end = text;
    var text = document.getElementById('remark').value;
    formdat.remark = text;
    jsondat.model = "myApp.family";
    jsondat.fields = formdat;
    console.log(jsondat);
    Familydat.db.table('Family').put(jsondat);

}

// URL末端の取得
getHTML_name = function() {
    return window.location.href.split('/')[4]+'/'+window.location.href.split('/')[5];
}
