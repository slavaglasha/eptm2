

var need_saved = false;

 function test(elclass){
    alert(elclass.object_name)
}


       function saveNewForm(objname,url_new){


        $("#newModal_wait").fadeIn(100);
         if (validNewForm()){
             if (true){

                 need_saved = false;

                 $.ajax({
                     type: "POST",
                     url: url_new,
                     data: $("#new-dictionary-form").serialize(),
                     success: function (json) {
                         if (json.success) {

                             $("#number-new").text(objname + json.name);
                             $("#new-form__message").removeClass("hidden").removeClass('alert-danger').children("p").text(objname+success_created);
                             need_saved = true;
                             $("#new-dictionary__btn-close").text(exit);
                             $("#save-new-dictionary").hide();
                             $("#new-dictionary__btn-new").show();
                             $("#newModal_wait").hide();
                         } else {
                             $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(objname+' '+error_created);
                             $.each(json.errors, function (key, item) {
                                 let id = item[0];
                                 let field = $("#new-dictionary-form").find("#id_" + item[0]);
                                 if (field !== undefined) setErrortext(field, item[1]);
                             });


                         }
                         $("#newModal_wait").fadeOut(100);
                         need_saved= true;

                     },
                     error: function (xhr, errmsg, err) {

                         $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(objname+' '+error_created+' '+error_text_messsage );

                         $("#newModal_wait").fadeOut(100);
                         need_saved= true;
                     }
                 });
             }

         }else {
             $("#newModal_wait").fadeOut(100);
         }
         $("#newModal_wait").fadeOut(100);
    }





    function loadNewForm(url_new, objname,LoadList){

        if ($("#cansave").text()=="True"){
            $("#newModal_wait").fadeIn(100);
            //$(container).html('');
            var container = $("#newModal").find(".main-block");
            if (container !== undefined && container !== null) {

                $("#number-new").text(objname);
                $.ajax({
                    type: "GET",
                    url: url_new,
                    cache: false,
                    success: (function (html) {

                        $(container).html(html);
                        // not need change form there are only text field and text area field
                        // connectArcticUser($("#new-request-form"), searchDep, clearDep);
                        setWidgetsSelect($("#new-dictionary-form"));

                        let el = $("#save-new-dictionary");

                        $("#save-new-dictionary").click(function () {
                            saveNewForm(objname, url_new)
                        });
                        $("#new-dictionary__btn-new");

                        $("#new-dictionary__btn-new").click(function () {
                            resetNewForm(objname);
                        });

                        /*$("#newForm").find(".main-block").find('form')[0].reset();/*loadNewRequestForm($("#newForm").find(".main-block"));*/
                        $("#save-new-dictionary").show();
                        $("#new-dictionary__btn-new").hide();
                        $("#new-dictionary__btn-new").text(new_obj + objname);


                        $("#btn-new-dictionary").html(new_obj + objname).click(function () {
                            $("#new-form-block").arcticmodal({
                                beforeOpen: function () {
                                    setStatusOpen()
                                },
                                afterClose: function () {
                                    reloadAfterSave(LoadList,objname)
                                }
                            });
                        });
                        $("#newModal_wait").fadeOut(100);


                    }),
                    error: function (xhr, errmsg, err) {

                        $(container).html("<div class='row'>  <div class='alert alert-danger' id='new-form__message'> <p>  " + error_text_messsage + err + "</p></div></div>");
                        $("#new-form-block").arcticmodal();
                        $("#newModal_wait").fadeOut(100);
                    }
                });
            }
        }
    }

    function resetNewForm(object_name){
        var container = $("#newModal").find(".main-block");
        $("#new-dictionary-form")[0].reset();
        $("#new-form-block").find(".number-new").html(new_obj+object_name);
        // var selected_text = $("#id_request_user").find(":selected").val();
        $("#save-new-dictionary").show();
        $("#new-dictionary__btn-new").hide();

        $("#new-form__message").hide();

        // var te = $("#new_form-user-name").text();
        //
        // $("#newForm").find("#id_request_user").next("span").find("input").val(te);

    }



     function validNewForm (){
         let result=true;

         let form=$("#new-dictionary-form");
         if (undefined !== form) {
            let el = $(form).find("#id_name");
           result = result && checkRequiredField(el);
         }
         return result;
    }

    function reloadAfterSave (updateList,object_name){

          updateList();
         if (need_saved){

             //loadNewRequestForm($("#newForm").find(".main-block"));
             resetNewForm(object_name);
             //$("#newForm").find(".main-block").find('form')[0].reset();


         }
     }

    function setStatusOpen(){
        need_saved=false;
     }


$(document).ready(function(){


});