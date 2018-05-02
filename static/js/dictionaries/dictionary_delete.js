var deleted = false;
function deleteObject(url_delete, id_object) {

     deleted  = false;
                        $.arcticmodal({
                            type: 'ajax',
                            url: url_delete + id_object + "/",
                            ajax: {
                                type: 'GET',
                                cache: false
                            },

                            beforeClose: function () {
                             //   $("#delete-form").hide();
                            },

                            afterLoadingOnShow: function (data, el) {
                                prepareButtonActions(url_delete,id_object);
                            },
                            errorLoading: function () {
                            },
                            afterClose: function () {


                                closeAfterDelete();

                            }


                        });
}


function prepareButtonActions(url_delete, id_object){
    $("#deleteButton").click(function(){
        deleted = false;

        $.ajax({
                    type: "post",
                    data: $("#deleted-form").serialize(),
                    cache: false,
                    url:url_delete + id_object + "/",
                    success: function (json) {

                       if (json.success){
                           $("#delete-form").removeClass("alert-danger");
                           $("#delete-form").find(".mess").addClass("small-alert").text(success_delete);

                           deleted = true;




                       }
                       else{

                            $("#delete-form").find("mess").text(error_delete+" "+json.error_message);
                           $("#delete-form").addClass("small-alert").addClass('alert-danger').find(".mess").text(error_delete_object+" "+json.error_message);
                            deleted = false;




                       }

                           $("#deleteButton").hide();
                           $("#delete-form").find("#cancelButton").text(exit);

                    },
                    error: function (xhr, errmsg) {


                        $("#delete-form").addClass('alert-danger').find(".mess").text(error_text_messsage+" "+error_delete_object);
                        $("#deleteButton").hide();
                        $("#delete-form").find("#cancelButton").text(exit);
                       deleted=false;
                       // $("#deleteModal_wait").fadeOut(100);

                    }
                });
    });
}

function closeAfterDelete(){

    if (deleted){
        $("#updateForm").arcticmodal('close');
    }
}