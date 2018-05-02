url_open="/dictionaries/users-list-json/";

let url_new ='/dictionaries/users-new/';
let object_name = 'Пользователь';
url_update =  "/dictionaries/users-update/";
url_delete  = "";

$(document).ready(function () {
 loadList(url_open,url_update, url_delete, object_name);
  loadNewForm(url_new,object_name,function(){loadList(url_open,url_update, url_delete,object_name)});


});