
class DictionaryOpen{
    constructor(url_new, object_name,updateList) {
        this.url_new = url_new;
        this.object_name = object_name;
        this.isLoaded = false;
        this.updateList = updateList;

        this.new_object_name = new_obj+object_name;
        this.newSaved = false;
        this.container = $("#newModal").find(".main-block");
        this.need_saved = true;
    }

    loadForm(){
         $("#newModal_wait").fadeIn(100);
        //$(container).html('');
        if (this.container!=undefined){
            let container = this.container;
            $("#number-new").text(this.new_object_name);
            $.ajax({
                type: "GET",
                url: this.url_new,
                cache: false,
                success: (function (html) {

                    $(container).html(html);
                    // not need change form there are only text field and text area field
                    // connectArcticUser($("#new-request-form"), searchDep, clearDep);
                    $("#save-new-dictionary").click(this.saveForm);
                    $("#new-dictionary__btn-new").click(function () {
                        this.resetForm();
                        /*$("#newForm").find(".main-block").find('form')[0].reset();/*loadNewRequestForm($("#newForm").find(".main-block"));*/
                    });
                    $("#save-new-dictionary").show();
                    $("#new-dictionary__btn-new").hide();
                    $("#new-dictionary__btn-new").text("this.new_object_name");

                    $("#btn-new-dictionary").click(function () {
                        $("#new-form-block").arcticmodal({
                            beforeOpen: setStatusOpen,
                            afterClose: this.reloadAfterSave
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

    resetForm(){
        $(this.container).find('form')[0].reset();
        $("#new-form-block").find(".number-new").html(this.new_object_name);
        // var selected_text = $("#id_request_user").find(":selected").val();
        $("#save-new-dictionary").show();
        $("#new-dictionary__btn-new").hide();

        $("#new-form__message").hide();

        // var te = $("#new_form-user-name").text();
        //
        // $("#newForm").find("#id_request_user").next("span").find("input").val(te);

    }

    saveForm(){
        $("#newModal_wait").fadeIn(100);
         if (this.validForm()){
             if (this.need_saved){

                 this.need_saved = false;

                 $.ajax({
                     type: "POST",
                     url: this.url_new,
                     data: $("#new-dictionary-form").serialize(),
                     success: function (json) {
                         if (json.success) {

                             $("#number-new").text(this.object_name + json.name);
                             $("#new-form__message").removeClass("hidden").removeClass('alert-danger').children("p").text(success_created);
                             this.newSaved = true;
                             $("#new-dictionary__btn-close").text(exit);
                             $("#save-new-dictionary").hide();
                             $("#new-dictionary__btn-new").show();
                             $("#newModal_wait").hide();
                         } else {
                             $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(error_created);
                             $.each(json.errors, function (key, item) {
                                 var id = item[0];
                                 var field = $("#new-dictionary-form").find("#id_" + item[0]);
                                 if (field !== undefined) setErrortext(field, item[1]);
                             });


                         }
                         $("#newModal_wait").fadeOut(100);
                         need_saved= true;

                     },
                     error: function (xhr, errmsg, err) {

                         $("#new-form__message").removeClass("hidden").addClass('alert-danger').children("p").text(error_created);

                         $("#newModal_wait").fadeOut(100);
                         this.need_saved= true;
                     }
                 });
             }

         }else {
             $("#newModal_wait").fadeOut(100);
         }
    }

    validForm(){

         let result=true;
         let form=$("#new-dictionary-form-form");
         let el=$(form).find("#id_name");
         result =  checkRequiredField(el) && result ;
         return result;



    }

    reloadAfterSave(data, el){

          this.updateList();
         if (this.newSaved){

             //loadNewRequestForm($("#newForm").find(".main-block"));
             this.resetForm();
             //$("#newForm").find(".main-block").find('form')[0].reset();


         }
     }

}