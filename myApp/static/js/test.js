//collect latest post from server and store in idb.
fetch('http://127.0.0.1:8000/getNFA/1/0/').then(function(response){
  return response.json();
}).then(function(arr){

    for(var obj of arr) {
        console.log(JSON.stringify(obj.fields));
      };
    })
