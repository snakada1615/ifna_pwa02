//----------------------------------

var Familydat = {
    db: null,
    renderer: function(Familydat) {
        var d = '';
        d += "        <div class='card border-primary col-12 mt-2' style='max-width: 540px;'>";
        d += "    		  <div class='row'>";
        d += "    		    <div class='col-4 d-flex align-items-center'>";
        d += "    		      <img src='../../../static/img/152053house192.png' %}" +" class='card-img'>";
        d += "    		    </div>";
        d += "    		    <div class='col-8'>";
        d += "    		      <div class='card-body bg-light p-2'>";
        d += "    		        <h5 class='card-title'>";
        d +=     							Familydat.fields.name;
        d += "    						</h5>";
        d += "    						<p class='card-text'>";
        d +=     							Familydat.fields.size;
        d += "    						</p>";
        d += "    						<p class='card-text'>";
        d +=     							Familydat.fields.remark;
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
};

// 初期化のメソッドを定義してみる
Familydat.initDB = function(db_name) {
    var request = indexedDB.open(db_name);

    // 「DBをopenするリクエスト」が成功に終われば、
    // 得られた結果はDBなので、保持しておく
    // あとはこの単一オブジェクトを使えばよろしい
    request.onsuccess = function (evt) {
        console.log('database opened');
        Familydat.db = (evt.target) ? evt.target.result : evt.result;
        // ま、ついでだしgetAllすっか
        //Familydat.getAll(Familydat.renderer);
    };

    request.onerror = function (evt) {
        console.log("IndexedDB error: " + evt.target.errorCode);
    };

    request.onupgradeneeded = function (evt) {
        db = evt.target.result;
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'FCT',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("FCT store created");
        }
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'DRI',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("DRI store created");
        }
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'DRI_w',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("DRI_w store created");
        }
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'Person',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("person store created");
        }
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'Crop',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("crop store created");
        }
        var objectStore = evt.currentTarget.result.createObjectStore(
                              'Family',
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("family store created");
        }

    };
}

Familydat.addIDB_web = function(dname, sname, sid) {
  return new Promise(function(resolve) {
    var r = window.indexedDB.open(dname)
    r.onupgradeneeded = function() {
      var idb = r.result
      var store = idb.createObjectStore(sname, {keyPath: "pk", autoIncrement: true})
      console.log('new store created');
    }
    r.onsuccess = function() {

      //collect latest post from server and store in idb.
      fetch('http://127.0.0.1:8000/getNFA/' + sid + '/').then(function(response){
        return response.json();
      }).then(function(arr){

        var idb = r.result
          let tactn = idb.transaction(sname, "readwrite")
      	  var store = tactn.objectStore(sname)
          if (store) {console.log(sname)};
          for(var obj of arr) {
            var req = store.put(obj)
            req.onsuccess = function () {
                //console.log('added');
            };
          }
          resolve(idb)
      })
      module.getAll(module.renderer);
    }

    r.onerror = function (e) {
     alert("Enable to access IndexedDB, " + e.target.errorCode)
    }
  })
}


// TODOを追加するメソッドを定義してみる
Familydat.addIDB_form = function(jsondata) {
    var db = Familydat.db;
    // DBからObjectStoreへのトランザクションを生成する
    // この段階で"todo"というObjectStoreをつくってないと
    // 当然、Table name not found に似たエラーを吐く
    var tx = db.transaction(["Family"],"readwrite");
    // このトランザクション内でアクティブなObjectを生成する
    var store = tx.objectStore("Family", {keyPath: "pk", autoIncrement: true});
    // putするリクエストを生成
    var req = store.put(jsondata);
    // 「putするリクエスト」が成功したら...
    tx.oncomplete = function() { console.log("noroi");; };
    // 「putするリクエスト」が失敗したら...
    tx.onerror = function(err) { console.log("xxx2", err); };
};

Familydat.test = function() {
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
  console.log(formdat);
  console.log(jsondat);
  Familydat.addIDB_form(jsondat);
  }


var req = Familydat.initDB('NFA-db');
if (req) {
  if (DBexists == false) {
    console.log('new store create');
    Familydat.importAll();
  } else {
    console.log('database already exists');
  };
}
