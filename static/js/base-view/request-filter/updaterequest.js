  function show_departure() {



        if ((!(isDate($("#id_receive_dateTime").val()))) || ( $("#update-request-form #id_receive_user").val()== "")) {
            $("#departures").hide();
        }

         $("#id_receive_dateTime").change(function(){
           enabledDeparture();
         });

         $("#update-request-form #id_receive_user").change(function(){
            enabledDeparture();
         });

         $("#add-departure").click(function(){
             cloneMore($("#empty-form"),"__prefix__");
         });

         $("input[id*='-id']").parent().parent().hide();
         $("input[id*='initial']").parent().parent().show();

         //$("input[id*='-DELETE']").parent().parent().hide();
         $("input[id*='-main_request']").parent().parent().hide();

         $("a[id*='del-']").click(function(){

         alert($(this).parent().parent().prev().find("input[id*='-DELETE']").attr("id"))
         $(this).parent().parent().prev().find("input[id*='-DELETE']").attr({"checked":true});
       });
    }








    function isDate(stringToValidate){

      var rgexp =/^([1-9]|([012][0-9])|(3[01])).([0]{0,1}[1-9]|1[012]).\d\d\d\d [012]{0,1}[0-9]:[0-6][0-9]$/;
      return rgexp.test(stringToValidate);
    }

    function enabledDeparture(){
        /*option:selected*/

        if((isDate($("#id_receive_dateTime").val()))&&( $("#update-request-form #id_receive_user").val().length>0) ){
            if ($("#departures").is(':hidden')) {
                $("#departures").toggle(10);
            }
        }else {
            if ($("#departures").is(':visible')) {
                $("#departures").toggle(10);
            }
        }
    }


 /*для копирования формы выезда!*/
  function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

   function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + prefix + '-', '-' + total + '-');


        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');

    });
    newElement.find('label').each(function() {
        var namef = $(this).attr('for').replace('-' + prefix + '-', '-' + total + '-');
        $(this).attr({'for': namef});

    });
    total++;
    $('#id_TOTAL_FORMS').val(total);
    var after_id="empty-form";
    if (total>1){
        after_id="form_departure-"+(total-1);
    }

    newElement.attr({"id":"form_departure-"+total});
    newElement.find(".dep-number").text(total);

    var id="#id-"+(total-1)+"-start_datetime";
    newElement.find(id).attr({"value":$("id_-__prefix__-start_datetime").attr('value')});
    newElement.find(id).text($("id_-__prefix__-start_datetime").attr('value'));
    newElement.append("<div class='row'><div class='col-4 col-offset-4'><a id='del--0' >Удалить</a>  </div></div>");
    newElement.find("#del--0").addClass("btn").addClass("btn-sm").addClass("btn-outline-secondary");
    newElement.find("#del--0").attr({"id":"del-"+(total-1)});
    alert("#id_-"+total+"-id");
    newElement.find("#id_-"+(total-1)+"-id").parent().parent().hide();
    newElement.find("#id_-"+(total-1)+"-DELETE").parent().parent().hide().next().hide();
    $('#empty-form').after(newElement);




    //$($("#add-dep-row")).toggle(newElement);
    /*$($("#add-dep-row")).toggle(newElement); /*перед кнопкой добавить*/
    /*var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>');*/
    return false;
}
$(document).ready(function() {

});