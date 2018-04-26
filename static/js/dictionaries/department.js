url_open="/dictionaries/departments-list-json/";

let url_new ='/dictionaries/departments-new/';
let object_department_name = 'Департамент';
url_update =  "/dictionaries/departments-update/";
url_delete  = "/dictionaries/department-delete/";

$(document).ready(function () {
 loadList(url_open,url_update, url_delete, object_department_name);
  loadNewForm(url_new,object_department_name,function(){loadList(url_open,url_update, url_delete,object_department_name)});


});