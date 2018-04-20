  var error_text_messsage = "Ошибка на сервере ";
  var required =  'Обязательное поле ';
  var invalid_dat= 'Введите правильный формат даты dd.mm.yyyy hh:mm';
  var success_created = 'Заявка успешно создана';
   var error_created = 'Заявка не создана';
  var exit = 'Выход';
  var cancel =  'Отмена';
  var rec_number = 'Заявка №';
  var new_request = 'Новая заявка';
  var need_saved = true;

  function setErrortext(field, text) {
         $(field).parent().parent().parent().addClass('invalid');
            $(field).parent().siblings('.error-text').html(text);
     }
  
 $(document).ready(function(){

     var newSaved=false;

     //устанвка даты
     function setNewRequestDate(){
         var now = new Date();
         var formated_date = now.format("dd.mm.yyyy hh:mm");
         $("#new-request-form").find("#id_request_dateTime").val(formated_date);
     }

     //установка пользователя
     function setUser(){
         if( $("#new-request-form").find("#id_request_user").val()==='' && $("#new-request-form").find("#id_request_outer_User").val()===''){
             $("#new-request-form").find("#id_request_user").val($("#id_user").html());
             searchDep($("#id_user").html(),$("#new-request-form"));
         }
     }



     function checkRequiredField(field ){

         if ($(field).val()===''){


            $(field).parent().parent().parent().addClass('invalid');
            $(field).parent().siblings('.error-text').html(required);
            return false;
         }else{
             $(field).parent().parent().parent().removeClass('invalid');
             return true;

         }
     }

     function validform() {
          var result=true;
         form=$("#new-request-form");
         var el=$(form).find("#id_request_user");
         result =  checkRequiredField(el) && result ;
         result =  checkRequiredField($(form).find("#id_request_outer_status")) && result ;
         result =  checkRequiredField($(form).find("#id_request_outer_department")) && result ;
         result = checkRequiredField($(form).find("#id_request_dateTime"))&& result ;
         result = checkRequiredField($(form).find("#id_place")) && result ;
         result = checkRequiredField($(form).find("#id_about")) && result ;
         return result;

     }

     function saveNewRequest(){
         $("#newModal_wait").fadeIn(100);
         if (validform()){
             if (need_saved){

                 need_saved = false;

                 $.ajax({
                     type: "POST",
                     url: "/base/new-request/",
                     data: $("#new-request-form").serialize(),
                     success: function (json) {
                         if (json.success) {

                             $("#number-new").text(rec_number + json.number);
                             $("#new-form__message").removeClass("hidden").removeClass('alert-danger').children("p").text(success_created);
                             newSaved = true;
                             $("#new-request__btn-close").text(exit);
                             $("#save-new-request").hide();
                             $("#new-request__btn-new").show();
                             $("#newModal_wait").hide();
                         } else {
                             $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(error_created);
                             $.each(json.errors, function (key, item) {
                                 var id = item[0];
                                 var field = $("#new-request-form").find("#id_" + item[0]);
                                 if (field !== undefined) setErrortext(field, item[1]);
                             });


                         }
                         $("#newModal_wait").fadeOut(100);
                         need_saved= true;

                     },
                     error: function (xhr, errmsg, err) {

                         $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(error_created);

                         $("#newModal_wait").fadeOut(100);
                         need_saved= true;
                     }
                 });
             }

         }else {
             $("#newModal_wait").fadeOut(100);
         }
     }

     function setStatusOpen(data, el){
         newSaved = false;
         stopTimerUpdae();

     }

     function reloadAfterSave(data, el){
         enableTimerUpdae();
         updateList();
         if (newSaved){

             //loadNewRequestForm($("#newForm").find(".main-block"));
             resetNewRequestForm();
             //$("#newForm").find(".main-block").find('form')[0].reset();


         }
     }

    // $("#save-new-request").click(function(){
    //
    //     $.ajax({
    //         type:"POST",
    //         url:"/new_request/",
    //         data:$("#new-request-form"),
    //         success: function (html) {
    //             $("#new-request-block").html(html);
    //
    //             connectArcticUser($("#newForm").find('form'));
    //         },
    //         error:function(xhr,errmsg,err){
    //
    //             $("#new-request-error-message").text(error_text_messsage+err)
    //         }
    //     })
    // })
    /*загрузим форму новой заявки*/
    function loadNewRequestForm(container) {
        $("#newModal_wait").fadeIn(100);
        //$(container).html('');

        $("#number-new").text(new_request);
        $.ajax({
            type: "GET",
            url: "/base/new-request/",
            cache: false,
            success: (function (html) {

                $(container).html(html);
                connectArcticUser($("#new-request-form"), searchDep, clearDep);
                $("#save-new-request").click(saveNewRequest);
                $("#new-request__btn-new").click(function(){resetNewRequestForm();/*$("#newForm").find(".main-block").find('form')[0].reset();/*loadNewRequestForm($("#newForm").find(".main-block"));*/});
                $("#save-new-request").show();
                $("#new-request__btn-new").hide();
                //$("#new-request__btn-close").click(close_new_request);
                $("#btn-new-request").click(function () {
                    $("#newForm").arcticmodal({
                        beforeOpen: setStatusOpen,
                        afterClose: reloadAfterSave
                    });
                });
                $("#newModal_wait").fadeOut(100);


            }),
            error: function (xhr, errmsg, err) {

                $(container).html(  "<div class='row'>  <div class='alert alert-danger' id='new-form__message'> <p>  " + error_text_messsage + err + "</p></div></div>");
                $("#newForm").arcticmodal();
                $("#newModal_wait").fadeOut(100);
            }
        });
    }


    function resetNewRequestForm(){
        $("#newForm").find(".main-block").find('form')[0].reset();
        $("#newForm").find(".number-new").html(new_request);
        var selected_text = $("#id_request_user").find(":selected").val();
        $("#save-new-request").show();
        $("#new-request__btn-new").hide();

        $("#new-form__message").hide();

        var te = $("#new_form-user-name").text();

        $("#newForm").find("#id_request_user").next("span").find("input").val(te);

    }
    loadNewRequestForm($("#newModal").find(".main-block"));

});