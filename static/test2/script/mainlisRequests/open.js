var correct_interval='Введите правильный интервал  дат';
var correct_number = ' Введите правильный номер';
var error_load_data='Ошибка загрузки данных!';
var error_messages_lg="НЕ загрузился фильтр";
var isLoaded=false;
var isTimerEnabled=true;
var timerUpdateListId;

function correctNumber(strnumber){
    if ((strnumber.trim())!==''){
        alert(strnumber);
        var re = /^\d+$/;
        return re.test(strnumber.trim());
    }else {
        return true;
    }
}
function  converttodate(dateString){
    //match date in format DD.MM.YYYY
      var  m = /^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20\d{2}) ([0-1]\d|[2][0-3])\:([0-5][0-9])$/.exec(dateString);

    if (m) {
        $("#result").html(true);

        var parts = dateString.split(' ');
        var dstr = parts[0], tstr = parts[1];
        var dparts = dstr.split('.'), tparts = tstr.split(':');

        return new Date(dparts[2], dparts[1] - 1, dparts[0], tparts[0], tparts[1]);
    }
    else{
        return 0;
    }


}


/*проверка дат с в строках должна біть дата dd.mm.yyyy hh:mm  в первой строке дата меньше чем во второй*/
function compareDate(str1, str2) {
    var date1=0, date2=0;
    if (str1.trim()!=="") {
        date1 = converttodate(str1);
        if (date1===0) {return false;}
    }
    if (str2.trim() === '') {
    } else {
        date2 = converttodate(str2);
        if (date2 === 0) {
            return false;
        }
    }
    return !(date1 !== 0 && 0 !== date2 && date1 > date2);


}
/*проверяет правильній ввод дат для формі фильтров  eldt1, eldt2  -  input  с датой dd.mm.yyyy hh:mm*/
function checkDateIntervalElementFilter(eldt1, eldt2 ){

     //Проверка ввода дат

     if (!compareDate($(eldt1).val(),$(eldt2).val())){

         $(eldt1).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');
         $(eldt2).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');

         $(eldt2).parent().siblings('.error-text').text(correct_interval).show();
         $(eldt1).parent().parent().parent().addClass("invalid");
         return false;

     }
     else {
         $(eldt1).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         $(eldt2).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         $(eldt2).parent().siblings('.error-text').text('').hide();
         $(eldt1).parent().parent().parent().removeClass("invalid");
         return true;
     }
 }

 function checkNumberElementFilter(eldt ){
    if (correctNumber($(eldt).val())){
       $(eldt).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
       $(eldt).parent().parent().parent().removeClass("invalid");
       $(eldt).parent().parent().siblings('.error-text').text('').hide();

       return true;
    } else{
        $(eldt).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');
        $(eldt).parent().parent().parent().addClass("invalid");
        $(eldt).parent().parent().siblings('.error-text').text(correct_number).show();
        return false;
    }

 }

 function   loadData(need_closed) {

         isLoaded=true;
        var id;

         $.ajax({
               type: "get",
               cache: false,
               url: "/test2/filter-request-json/",
               data: $('#filterForm').find('form').serialize(),
               success:function(json){
                   if (json.success) {
                       $.each(json.requests, function (key, item) {
                           if (item!==null) {
                               var newrow = $("#first-row").clone();
                               $.each(item, function (inkey, val) {
                                   $(newrow).find("." + inkey).html(val);

                               });
                           }
                           if (item!==null) {
                               var deps;
                               deps = item.departures;
                               $.each(deps, function (inkey, val) {

                                   $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.start + "</small>")
                                   $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.end + "</small>")
                                   $(newrow).find(".departures").append("<span class=\"d-block\">" + val.users + "</span>")
                               });
                               $(newrow).attr('id', 'row-' + item.id).removeClass("hidden");
                               $("#main-list").append(newrow);
                               id = item.id;
                           }


                       });
                       var last_el = $("#first-row");
                       $.each(json.new_requests, function (key, item) {
                           var newrow = $("#first-row").clone();
                           $.each(item, function (inkey, val) {
                               $(newrow).find("." + inkey).html(val);

                           });
                           var deps;
                           deps = item.departures;
                           $.each(deps, function (inkey, val) {

                               $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.start + "</small>");
                               $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.end + "</small>");
                               $(newrow).find(".departures").append("<span class=\"d-block\">" + val.users + "</span>")
                           });
                           $(newrow).attr('id', 'row-' + item.id).removeClass("hidden");
                           $(last_el).after(newrow);

                           last_el = newrow;


                       });
                       if (json.changed_requests!==undefined) {
                           $.each(json.changed_requests, function (key, item) {
                               var currow = $("#main-list").find("#row-" + item.id);
                               if (currow !== undefined) {
                                   $.each(item, function (inkey, val) {
                                       $(currow).find("." + inkey).html(val);

                                   });
                                   var deps;
                                   deps = item.departures;
                                   $(currow).find(".departures").html("");
                                   $.each(deps, function (inkey, val) {

                                       $(currow).find(".departures").append("<small class=\"text-muted d-block\">" + val.start + "</small>");
                                       $(currow).find(".departures").append("<small class=\"text-muted d-block\">" + val.end + "</small>");
                                       $(currow).find(".departures").append("<span class=\"d-block\">" + val.users + "</span>")
                                   });
                               }


                           });
                       }
                       var filterForm = $('#filterForm');
                       $(filterForm).find("#last-id").val(id);
                       $(filterForm).find("#last-dt").val(json.dt);
                       need_more = json.max_rows === json.requests.length;

                       setRowUpdater(); //установка собітия на строки окно просмотра заявок
                       $("#wait").fadeOut(100);
                       if (need_closed !== undefined) {
                           if (need_closed === true) {
                               $(filterForm).arcticmodal('close');
                           }
                       }
                       isLoaded = false;
                       setTimeUpdate();

                   }





               },
               error: function (xhr, errmsg ) {
                $(".wait-block").html(error_load_data + '-'+errmsg);
                isLoaded= false;

            }
           });


 }

 function updateList() {
     if (!isLoaded && isTimerEnabled) {
         isLoaded = true;
         $.ajax({
             type: "get",
             cache: false,
             url: "/test2/filter-request-json/",
             data: $('#filterForm').find('form').serialize(),
             success: function (json) {
                 if (json.success) {
                     var last_el = $("#first-row");
                     $.each(json.new_requests, function (key, item) {
                         var newrow = $("#first-row").clone();
                         $.each(item, function (inkey, val) {
                             $(newrow).find("." + inkey).html(val);

                         });
                         var deps;
                         deps = item.departures;
                         $.each(deps, function (inkey, val) {

                             $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.start + "</small>");
                             $(newrow).find(".departures").append("<small class=\"text-muted d-block\">" + val.end + "</small>");
                             $(newrow).find(".departures").append("<span class=\"d-block\">" + val.users + "</span>")
                         });
                         $(newrow).attr('id', 'row-' + item.id).removeClass("hidden");
                         $(last_el).after(newrow);

                         last_el = newrow;


                     });
                     $.each(json.changed_requests, function (key, item) {
                         var currow = $("#main-list").find("#row-" + item.id);
                         if (currow !== undefined) {
                             $.each(item, function (inkey, val) {
                                 $(currow).find("." + inkey).html(val);

                             });
                             var deps;
                             deps = item.departures;
                             $(currow).find(".departures").html("");
                             $.each(deps, function (inkey, val) {

                                 $(currow).find(".departures").append("<small class=\"text-muted d-block\">" + val.start + "</small>");
                                 $(currow).find(".departures").append("<small class=\"text-muted d-block\">" + val.end + "</small>");
                                 $(currow).find(".departures").append("<span class=\"d-block\">" + val.users + "</span>")
                             });
                         }


                     });
                     var filterForm = $('#filterForm');

                     if (json.dt !== undefined) {
                         $(filterForm).find("#last-dt").val(json.dt);
                     }
                     setRowUpdater(); //установка собітия на строки окно просмотра заявок
                     isLoaded = false;
                     setTimeUpdate();


                 }else{
                     isTimerEnabled=false;
                     stopTimerUpdae();
                 }
             }
             ,
             error: function (xhr, errmsg) {
                 $(".wait-block").html(error_load_data + '  - ' + errmsg);
                 isLoaded = false;
                 isTimerEnabled=false;
                 stopTimerUpdae();

             }
         });
     }

 }

 function setTimeUpdate() {
     var interval = 1;
     timerUpdateListId = setTimeout(updateList,interval*60*1000);
     isTimerEnabled = true;


 }

 function stopTimerUpdae() {
     if (timerUpdateListId!==undefined) {
         clearTimeout(timerUpdateListId);
     }
     isTimerEnabled = false;
 }

 function enableTimerUpdae() {
     isTimerEnabled = true;
 }

 function DoFilter(need_closed){
     if (need_closed=== undefined){
         need_closed = false;
     }
   //  $("#wait").fadeIn(100);
     if (checkfilter() !== true) {
     } else {
         $("#wait").fadeIn(100);
         $("#main-list").find(">:not(#first-row)").remove();

         $('#filterForm').find("#last-id").val(0);

         loadData(need_closed);


     }
 }

 function checkfilter(){

     //Проверка ввода дат

     var mainForm;
     mainForm = $('#filterForm');
     var eldt1=$(mainForm).find("#id_input_datetime_0");
     var eldt2=$(mainForm).find("#id_input_datetime_1");
     var result= checkDateIntervalElementFilter(eldt1,eldt2);

     eldt1=$(mainForm).find("#id_request_dateTime_0");
     eldt2=$(mainForm).find("#id_request_dateTime_1");
     result=result && checkDateIntervalElementFilter(eldt1,eldt2);

     eldt1=$(mainForm).find("#id_close_dateTime_0");
     eldt2=$(mainForm).find("#id_close_dateTime_1");
     result=result && checkDateIntervalElementFilter(eldt1,eldt2);
     // language=JQuery-CSS
     result=result &&checkNumberElementFilter($(mainForm).find("#id_number"));

    return result;


 }


 $(document).ready(function() {

 // function addRangeClasses(id_rifst){
 //     $('#'+id_rifst+'_0').addClass('col-6').next().addClass("divider").parent().addClass('form-inline');
 //     $('#'+id_rifst+'_1').addClass('col-5');
 // }


 function loadFilterForm() {
     var isload;
     isload = false;
     $.ajax({
               type: "get",
               cache: false,
               url: "/test2/filter-request-json/",
               data: {get_form:true},
               success:function(htmll){


                   var el =  $('#filter-container');
                   $(el).html(htmll);
                   connectArcticUser($(el).find('form'));
                   $("#do-filter").click(function (){DoFilter(true); });
                   $("#btn-update-list").click(function(){updateList();});
                   setTimeUpdate();
                   //preparefilterForm();

                   /*if (func!=undefined){func();}*/

                   isload=loadData();

                   /*initWidgets();
                   connectUser($("#new-request-form"));
                   initSelectNew();*/

                   // $('#newRequestModal').find('form').show();
                  // $('#newRequestModal').find('form').addClass("form-show");

               },
               error: function (xhr, errmsg ) {


                   $("#filter-container").text(error_messages_lg + errmsg);
                    isload=false;
            }
           });
      return isload;
 }
/*нудно подождать пока загрузится форма фильтра*/











    $("#open-filter").click(function () {
      //  $('#flex-container').hide();
         $("#filterForm").arcticmodal();
         stopTimerUpdae();

    });

    $("#scrolled-table").scroll(function () {
        var main_list =$("#main-list");
        if ($(main_list ).find(".row:last-child").position().top+$(main_list ).find(".row:last-child").height()<$("#scrolled-table").next().position().top) {
            if (!isLoaded && need_more ) {
                isLoaded=true;

                loadData();


            }
        }
    });

    $("#btn-new-request").click(function(){
        var main_list = $("#main-list");
        if ($(main_list).find(".row:last-child").position().top+$(main_list).find(".row:last-child").height()<$("#scrolled-table").next().position().top){
        }

        /*alert($("#scrolled-table").scrollTop()+" \t "+$("#scrolled-table").position().top +"\t"+$("#scrolled-table").next().position().top+"\t\t"+($("#main-list .row:last-child").position().top+$("#main-list .row:last-child").height()));*/
    });

 loadFilterForm();
 isLoaded=true;


 });
