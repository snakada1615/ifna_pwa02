
function contentLoaded() {
    db_name = "NFA-db";
    store_name = "FCT";
    key = 'pk';
    initDb();
}

function initDB(db_name, store_name) {
    var request = indexedDB.open(db_name);
    request.onsuccess = function (evt) {
        console.log('database opened');
        db = request.result;
    };

    request.onerror = function (evt) {
        console.log("IndexedDB error: " + evt.target.errorCode);
    };

    request.onupgradeneeded = function (evt) {
        var objectStore = evt.currentTarget.result.createObjectStore(
                              store_name,
                              {keyPath:'pk', autoIncrement: true}
                          );
        if (objectStore) {
          console.log("store created");
        }
    };
}


function importIDB(dname, sname) {
  return new Promise(function(resolve) {
    var r = window.indexedDB.open(dname)
    r.onupgradeneeded = function() {
      var idb = r.result
      var store = idb.createObjectStore(sname, {keyPath: "pk", autoIncrement: true})
      console.log('new store created');
    }
    r.onsuccess = function() {

      //collect latest post from server and store in idb.
      fetch('http://127.0.0.1:8000/getdata').then(function(response){
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
    }

    r.onerror = function (e) {
     alert("Enable to access IndexedDB, " + e.target.errorCode)
    }
  })
}
