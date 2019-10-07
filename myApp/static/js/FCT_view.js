//----------------------------------
var FCTdat = {
    db: null,
    renderer: function(FCTdat) {
        var d = '';
        d += "<tr>";
        d += "  <td>" + FCTdat.fields.Food_name + "</td>";
        d += "  <td>" + FCTdat.fields.Protein + "</td>";
        d += "  <td>" + FCTdat.fields.FE + "</td>";
        d += "  <td>" + FCTdat.fields.VITA_RAE + "</td>";
        d += "</tr>";

        var tr = document.createElement('tr');
        tr.innerHTML = d;
        document.getElementById("FCT-list").appendChild(tr);
    }
};

// 初期化のメソッドを定義してみる
FCTdat.initDB = function(db_name) {
    var request = indexedDB.open(db_name);

    // 「DBをopenするリクエスト」が成功に終われば、
    // 得られた結果はDBなので、保持しておく
    // あとはこの単一オブジェクトを使えばよろしい
    request.onsuccess = function (evt) {
        console.log('database opened');
        FCTdat.db = (evt.target) ? evt.target.result : evt.result;
        // ま、ついでだしgetAllすっか
        FCTdat.getAll(FCTdat.renderer);
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

FCTdat.addIDB = function(dname, sname, sid) {
  return new Promise(function(resolve) {
    var r = window.indexedDB.open(dname)
    r.onupgradeneeded = function() {
      var idb = r.result
      var store = idb.createObjectStore(sname, {keyPath: "pk", autoIncrement: true})
      console.log('new store created');
    }
    r.onsuccess = function() {

      //collect latest post from server and store in idb.
      fetch('http://127.0.0.1:8000/getNFA/' + sid+ '/').then(function(response){
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
FCTdat.addTodo = function(jsondata) {
    var db = FCTdat.db;
    // DBからObjectStoreへのトランザクションを生成する
    // この段階で"todo"というObjectStoreをつくってないと
    // 当然、Table name not found に似たエラーを吐く
    var tx = db.transaction(["FCT"],"readwrite");
    // このトランザクション内でアクティブなObjectを生成する
    var store = tx.objectStore("FCT");
    // putするリクエストを生成
    var req = store.put(jsondata);
    // 「putするリクエスト」が成功したら...
    tx.oncomplete = function() { FCTdat.getAll(FCTdat.renderer); };
    // 「putするリクエスト」が失敗したら...
    tx.onerror = function(err) { console.log("xxx2", err); };
};


// TODOをすべて取得するメソッドを定義してみる
FCTdat.getAll = function(renderer) {
    if (renderer) document.getElementById('FCT-list').innerHTML = '';
    // このへんは同じ
    var db = FCTdat.db;
    var tx = db.transaction(["FCT"],"readwrite");
    var store = tx.objectStore("FCT");
    // keyPathに対して検索をかける範囲を取得
    var range = IDBKeyRange.lowerBound(0);
    // その範囲を走査するカーソルリクエストを生成
    var cursorRequest = store.openCursor(range);
    // カーソルリクエストが成功したら...
    cursorRequest.onsuccess = function(e) {
        var result = e.target.result;
        // 注）走査すべきObjectがこれ以上無い場合
        //     result == null となります！
        if (!!result == false) return;
        // ここにvalueがくる！
        console.log(result.value);
        if (renderer) renderer(result.value);
        // カーソルを一個ずらす
        result.continue();
    }
    // カーソルリクエストが失敗したら...
    cursorRequest.onerror = function(err) {
        console.log("XXX3", err);
    }
};

FCTdat.add = function() {
    var text = document.getElementById('todo-text').value;
    FCTdat.addTodo(text);
};

var req = FCTdat.initDB('NFA-db');
if (req) {
  if (DBexists == false) {
    console.log('new store create');
    FCTdat.importAll();
  } else {
    console.log('database already exists');
  };
}
