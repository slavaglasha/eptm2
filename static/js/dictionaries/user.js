url_open="/dictionaries/users-list-json/";

let url_new ='/dictionaries/user-new/';
let object_name = 'Пользователь';
url_update =  "/dictionaries/user-update/";
url_delete  = "/dictionaries/user-delete/";

$(document).ready(function () {
 loadList(url_open,url_update, url_delete, object_name);
  loadNewForm(url_new,object_name,function(){loadList(url_open,url_update, url_delete,object_name)});


});