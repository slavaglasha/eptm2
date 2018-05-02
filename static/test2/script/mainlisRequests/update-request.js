 var success_update = 'Заявка успешно сохранена';
 var error_update = 'Заявка не сохранена';
 var closed_request = 'Заявка закрыта';
var ischanged=false;
var opened = false;


function getCurrentDateTime(){
    var date = new Date();
    var options = {
	year: 'numeric',
	month: 'numeric',
	day: 'numeric',
    hour:'numeric',
    minute:'numeric',
	timezone: 'UTC'
    };

    return ((new Date()).toLocaleString("ru", options).replace(',',''));

}



function setRowUpdater(){
        $.each( $("#main-list").find(".row"),
            function(){
                $(this).unbind();
                $(this).click(        function(){
                // после прокрутки внгихз а потом вверх срабатіваетнесколько раз собітие нажатия на кнопку!
                stopTimerUpdae();
                    if (opened !== false) {
                    } else {
                        var id = $(this).find(".id").html();
                        opened = true;
                        $.arcticmodal({
                            type: 'ajax',
                            url: "/base/update-request/" + id + "/",
                            ajax: {
                                type: 'GET',
                                cache: false
                            },
                            beforeClose: function () {
                                $("#updateForm").hide();
                            },

                            afterLoadingOnShow: function (data, el) {
                                prepareUpdateForm();
                            },
                            errorLoading: function () {
                            },
                            afterClose: function () {
                                opened = false;
                                enableTimerUpdae();
                                updateList();
                                if (ischanged === true) {
                                    reloadAfterSave();
                                }
                            }


                        });
                    }
            });
        });

}

function prepareUpdateForm(){
    ischanged = false;
    if ($(".arcticmodal-container").length>1){
         $(".arcticmodal-container")[1].remove();
         $(".arcticmodal-overlay")[1].remove();
     }
    connectArcticUser($("#update-from-main-form"),searchDep, clearDep);
    enabledDepartures();

    searchDep($("#updateForm").find("#id_request_user").val(),$("#update-request-form"));
    $("#updateForm").find("#id_receive_user").on("selectmenuchange",function(event, ui){

        changeReceiveUser($("#updateForm").find("#id_receive_user").val());
    });
    $("#updateForm").find("#save-update-request").unbind();
    $("#updateForm").find("#save-update-request").click(saveUpdateRequest);
    $("#updateModal_wait").fadeOut(100);
    $("#add-departure").unbind();
    $("#add-departure").click(function(){
             cloneMore($("#empty-form"),"__prefix__");
         });

     $("div [id*='form_departure']").each(function () {
       setWidgets(this);
     });
     setClosedStatus();
}

function enabledDepartures(){


    if ($("#updateForm").find("#id_receive_user").val()!==""){
        $("#empty-form").hide();
        $("#departures").fadeIn(10);

    }else {
        $("#empty-form").hide();
        $("#departures").fadeOut(10);
    }
    $("input[id$='DELETE']").hide();
    $("label[for$='DELETE']").hide();
    $("label[for$='-id']").hide();
    $("label[for$='main_request']").hide();
}

function changeReceiveUser(val) {

   if (val!==''){
       $("#updateForm").find("#id_receive_dateTime").val(getCurrentDateTime());
        $("#departures").fadeIn(10);

   }else{
       $("#updateForm").find("#id_receive_dateTime").val("");
        $("#departures").fadeOut(10);
   }
}

function validForm() {
    return true;
}

function saveUpdateRequest() {
        var id = $("#id").text();
         // language=JQuery-CSS
         $("#updateModal_wait").fadeIn(100);
         if (validForm()){
             $.ajax({
                    type: "post",

                    data: $("#update-request-form").serialize(),
                    cache: false,
                    url: "/base/update-request/" + id + "/",
                    success: function (json) {
                        $(".error-text").html("");
                        $(".invalid").removeClass('invalid');
                       if (json.success){
                           $("#update-form__message").removeClass('alert-danger').find("p").text(success_update);
                           $("#update-form__message").arcticmodal();
                           setClosedStatus();
                       }
                       else{
                           $("#update-form__message").addClass('alert-danger').find("p").text(error_update);
                           $.each(json.errors, function(key, item) {
                              var id= item[0];
                              var field =  $("#update-request-form").find("#id_"+item[0]);
                              if (field!==undefined)   setErrortext(field, item[1]);
                          });
                           var num=0;
                           $.each(json.departures_errors, function (key, val) {


                               $.each(val.departures, function (key, er_vals) {

                                   $.each(er_vals, function (fieldname, value) {

                                       var field_inner = $("#id_departure_set-"+key+'-'+fieldname);
                                       if (!field_inner!=undefined) setErrortext(field_inner, value);
                                   })


                               });

                           });
                           $("#update-form__message").arcticmodal();
                           /*$.each(json.departures_errors[0].departures, function (dep_errors) {
                              $.each(dep_errors, function (key, item) {
                                  var pref = '-'+num;
                                  alert(key);
                                  alert(pref);
                              });
                              num+=1;
                           });*/

                       }
                       $("#updateModal_wait").fadeOut(100);
                       ischanged = true;
                    },
                    error: function (xhr, errmsg) {


                        $("#update-form__message").addClass('alert-danger').find("p").text(error_text_messsage);
                        $("#update-form__message").arcticmodal();
                        $("#updateModal_wait").fadeOut(100);

                    }
                });


         }else {
             $("#updateModal_wait").fadeOut(100);
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
    var total = $('.departure-part-form').length-1;
    var oldElem = $('.departure-part-form').last();
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
    $('#id_departure_set-TOTAL_FORMS').val(total);
    var after_id="empty-form";
    if (total>1){
        after_id="form_departure-"+(total-1);
    }

    newElement.attr({"id":"form_departure-"+total});
    newElement.find(".dep-number").text(total);

    var id="#id-"+(total-1)+"-start_datetime";
  //  newElement.find(id).attr({"value":$("id_-__prefix__-start_datetime").attr('value')});
  //  newElement.find(id).text($("id_-__prefix__-start_datetime").attr('value'));

       var strDate = getCurrentDateTime();
       newElement.find(id).val(strDate);
       newElement.find(id).text(getCurrentDateTime());

    //newElement.append("<div class='row'><div class='col-4 col-offset-4'><a id='del--0' >Удалить</a>  </div></div>");
    //newElement.find("#del--0").addClass("btn").addClass("btn-sm").addClass("btn-outline-secondary");
    //newElement.find("#del--0").attr({"id":"del-"+(total-1)});
    //alert("#id_-"+total+"-id");
    newElement.find("#id_-"+(total-1)+"-id").parent().parent().hide();
    newElement.find("#id_-"+(total-1)+"-DELETE").parent().parent().hide().next().hide();
    $(oldElem).after(newElement);
    $(newElement).find("#id_-"+total+"-start_datetime").val(getCurrentDateTime());
    setWidgets(newElement);
    newElement.show();
    $("input[id$='DELETE']").hide();
    $("label[for$='DELETE']").hide();
    $("label[for$='-id']").hide();
    $("label[for$='main_request']").hide();





    return false;
}

function reloadAfterSave(data, el){

         if (ischanged){
             //DoFilter();



         }
 }

 function setClosedStatus(){
    if ($("#id_close_user").val() !== "" || $("#id_close_dateTime").val()!==""){
         $(".status-closed").html(closed_request);
         $("#add-departure").hide();
    }
    else{
         $(".status-closed").html('');
          $("#add-departure").show();
     }

 }

$(document).ready(function() {
 opened = false;
 ischanged = false;
});