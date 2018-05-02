let ischanged = false;
let opened = false;


function setRowUpdaterObject(url_update,url_delete, updateList, objname){
    if ($("#cansave").text()=="True") {
        $.each($("#main-list").find(".row"),
            function () {
                $(this).unbind();
                $(this).click(function () {
                    // после прокрутки внгихз а потом вверх срабатіваетнесколько раз собітие нажатия на кнопку!

                    if (opened !== false) {
                    } else {
                        let id = $(this).find(".id").html();

                        opened = true;
                        $.arcticmodal({
                            type: 'ajax',
                            url: url_update + id + "/",
                            ajax: {
                                type: 'GET',
                                cache: false
                            },
                            beforeClose: function () {
                                $("#updateForm").hide();
                            },

                            afterLoadingOnShow: function (data, el) {
                                prepareUpdateObjectForm(url_update, url_delete, objname, id);
                            },
                            errorLoading: function () {
                            },
                            afterClose: function () {
                                opened = false;

                                updateList();

                            }


                        });
                    }
                });
            });
    }

}

function prepareUpdateObjectForm(url_update, url_delete,objname, objid){
    setWidgetsSelect($("#update-object-form"));
    ischanged = false;
     $("#updateForm").find("#save-object-update").unbind();
    $("#updateForm").find("#save-object-update").click(function(){saveUpdateObject(url_update,objname)});
     if (url_delete!=='') {
           $("#updateForm").find("#delete-object").show();
         $("#updateForm").find("#delete-object").unbind().click(function () {
             deleteObject(url_delete, objid)
         });
     }else{
         $("#updateForm").find("#delete-object").hide();
    }
    $("#updateModal_wait").fadeOut(100);
    $("#updateModal_wait").fadeOut(100);

}

function saveUpdateObject(url_update,objname) {
    objname = $("#objname").text();
        var id = $("#id").text();
         // language=JQuery-CSS
         $("#updateModal_wait").fadeIn(100);
         if (true){
             $.ajax({
                    type: "post",

                    data: $("#update-object-form").serialize(),
                    cache: false,
                    url:url_update + id + "/",
                    success: function (json) {
                        $(".error-text").html("");
                        $(".invalid").removeClass('invalid');
                       if (json.success){
                           $("#update-inline-form__message").removeClass('alert-danger').find("p").text(objname+' '+success_update_object);
                           if  ($("#obj-name")!==undefined){
                               $("#obj-name").text(json.name);
                           }
                          // $("#update-form__message").arcticmodal();
                           $("#update-inline-form__message").show();

                       }
                       else{
                           $("#update-inline-form__message").addClass('alert-danger').find("p").text(objname+' '+error_update_object).show();
                           $.each(json.errors, function(key, item) {
                              var id= item[0];
                              var field =  $("#update-object-form").find("#id_"+item[0]);
                              if (field!==undefined)   setErrortext(field, item[1]);
                          });
                          // $("#update-form__message").arcticmodal();


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


         }


}