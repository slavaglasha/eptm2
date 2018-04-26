url_open="/dictionaries/places-list-json/";

let url_new ='/dictionaries/places-new/';
let object_name = 'Обьект';
url_update =  "/dictionaries/places-update/";
url_delete  = "/dictionaries/places-delete/";

$(document).ready(function () {
 loadList(url_open,url_update, url_delete, object_name);
  loadNewForm(url_new,object_name,function(){loadList(url_open,url_update, url_delete,object_name)});


});