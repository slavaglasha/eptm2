function correctNumber(strnumber){
    var re = /^\d[0-9]+\d$/;
    return re.test(strnumber);
}
function  converttodate(dateString){
    //match date in format DD.MM.YYYY
      var  m = /^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20\d{2}) ([0-1]\d{1}|[2][0-3])\:([0-5][0-9])$/.exec(dateString);

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

function correctNumber(numberString){
    var m=/^([1-9]d{})/
}
/*проверка дат с в строках должна біть дата dd.mm.yyyy hh:mm  в первой строке дата меньше чем во второй*/
function compareDate(str1, str2) {
    var date1=0, date2=0;
    if (str1.trim()!="") {
        date1 = converttodate(str1);
        if (date1===0) {return false;}
    }
    if (str2.trim()!=''){
        date2 = converttodate(str2);
        if (date2===0) {return false;}
    }
    if(date1!=0 && date2!=0 && date1>date2){
        return false;
    }
    return true;

}
/*проверяет правильній ввод дат для формі фильтров  eldt1, eldt2  -  input  с датой dd.mm.yyyy hh:mm*/
function checkDateIntervalElementFilter(eldt1, eldt2 ){

     //Проверка ввода дат

     if (!compareDate($(eldt1).val(),$(eldt2).val())){

         $(eldt1).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');
         $(eldt2).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');

         $(eldt2).next('.invalid-feedback').text('Введите правильную интервал  дат').show();
         return false;

     }
     else {
         $(eldt1).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         $(eldt2).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         return true;
     }
 }


 $(document).ready(function() {

 var isLoaded=false;
 function addRangeClasses(id_rifst){
     $('#'+id_rifst+'_0').addClass('col-6').next().addClass("divider").parent().addClass('form-inline');
     $('#'+id_rifst+'_1').addClass('col-5');
 }
 function preparefilterForm(){
     filter_initWidjects2("filter-container");
     $("#filterModal").find("#id_input_user").selectmenu();
     $("#id_receive_user").selectmenu();
     $("#id_close_user").selectmenu();
     $(".ui-selectmenu-button").addClass("form-control form-control-sm mr-sm-0");
     $("#filterModal").find("#id_number").spinner();

     addRangeClasses('id_input_datetime');
     addRangeClasses('id_request_dateTime');
     addRangeClasses('id_close_dateTime');
     addRangeClasses('id_receive_dateTime');
     $("#do-filter").click(DoFilter);
 }

 function loadFilterForm() {
     var isload, need_more;
     isload = false;
     need_more = true;
      $.ajax({
               type: "get",
               cache: false,
               url: "/test2/filter-request-json/",
               data: {get_form:true},
               success:function(htmll){


                   $('#filter-container').html(htmll);
                   connectUser($('#filter-container').find('form'));

                   preparefilterForm();

                   /*if (func!=undefined){func();}*/

                   isload=loadData();

                   /*initWidgets();
                   connectUser($("#new-request-form"));
                   initSelectNew();*/

                   // $('#newRequestModal').find('form').show();
                  // $('#newRequestModal').find('form').addClass("form-show");

               },
               error: function (xhr, errmsg ) {

                   var error_messages_lg="НЕ загрузился фильтр";
                   $("#filter-container").text(error_messages_lg + errmsg);
                    isload=false;
            }
           });
      return isload;
 }
/*нудно подождать пока загрузится форма фильтра*/
 function   loadData() {

         isLoaded=true;
        var id;

         $.ajax({
               type: "get",
               cache: false,
               url: "/test2/filter-request-json",
               data: $('#filterModal form').serialize(),
               success:function(json){

                    $.each(json.requests, function(key, item) {
                        var newrow =$("#first-row").clone();
                        $.each(item , function (inkey, val) {
                            $(newrow).find("."+inkey).html(val);
                        });
                        $(newrow).attr('id','row-'+item.id ).removeClass("hidden");
                        $("#main-list").append(newrow);
                        id=item.id;
                        isLoaded=false;



                    });
                    $('#filter-container').find("#last-id").val(id);
                    $('#filter-container').find("#last-dt").val(json.dt);
                    if (json.max_rows===json.requests.length){
                        need_more=true;
                    }else{
                        need_more=false;
                    }
                    var el = $("#last-id");
                     $("#wait").fadeOut(100);





               },
               error: function (xhr, errmsg ) {
                $(".wait-block").html('Ошибка загрузки данных!');
                isLoaded= false;

            }
           });


 }

 function checkfilter(){

     //Проверка ввода дат

     var mainForm = $('#filter-container');
     var eldt1=$(mainForm).find("#id_input_datetime_0");
     var eldt2=$(mainForm).find("#id_input_datetime_1");
     var result= checkDateIntervalElementFilter(eldt1,eldt2);

     eldt1=$(mainForm).find("#id_request_dateTime_0");
     eldt2=$(mainForm).find("#id_request_dateTime_1");
     result=result && checkDateIntervalElementFilter(eldt1,eldt2);

     eldt1=$(mainForm).find("#id_close_dateTime_0");
     eldt2=$(mainForm).find("#id_close_dateTime_1");
     result=result && checkDateIntervalElementFilter(eldt1,eldt2);

    return result;


 }
 function DoFilter(){
     if (checkfilter()) {
         $("#wait").fadeIn(100);
         $("#main-list").find(">:not(#first-row)").remove();

         $('#filter-container').find("#last-id").val(0);
         $("#filterModal").modal('hide');
         loadData();

     }
 }








    $("#open-filter").click(function () {
         $("#filterModal").modal('show');

    });

    $("#scrolled-table").scroll(function () {
        if ($("#main-list .row:last-child").position().top+$("#main-list .row:last-child").height()<$("#scrolled-table").next().position().top) {
            if (!isLoaded && need_more ) {
                isLoaded=true;

                loadData();


            }
        }
    });

    $("#btn-new-request").click(function(){
        var str='Not';
        if ($("#main-list .row:last-child").position().top+$("#main-list .row:last-child").height()<$("#scrolled-table").next().position().top){
            str='Load';
        }
        alert(str);
        /*alert($("#scrolled-table").scrollTop()+" \t "+$("#scrolled-table").position().top +"\t"+$("#scrolled-table").next().position().top+"\t\t"+($("#main-list .row:last-child").position().top+$("#main-list .row:last-child").height()));*/
    });

  var re = loadFilterForm();
 isLoaded=true;

 });
