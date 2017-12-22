$(document).ready(function() {
    var error_text_messsage = "Ошибка на сервере ";
    var error_text_message_valid = "Ошибка обработки данных!! ";
    var error_valid_filterform = '';


    function getFilterAjaxValidErrorFilterForm(html) {
        $("#filter-form-content").html(html);
        $("#save-filter").click(function () {
            saveFilter(getFilterAjaxValidErrorFilterForm, getFilterAjaxServerErrorFilterForm);
        });
        filter_initWidjects();
    }


    function getFilterAjaxServerErrorFilterForm(xhr, errmsg, err) {
        $("#error-message").show().text("Мы не можем обработать  данные! " + errmsg + xhr + err);
    }

    function getFilterAjaxValidErrorMainForm() {
        $("#main-form_error").show().text(error_text_message_valid);
    }

    function getFilterAjaxServerErrorMainForm( errmsg) {
        $("#error-message").show().text(error_text_message + " " + errmsg);
    }


    function saveFilter(validError, serverError) {
        $("#error-message").hide();
        $("#main-form_error").hide();
        $.ajax({
            type: "get",
            cache: false,
            url: "/filter_request/",
            data: $("#filter-form").serialize(),
            success: function (html) {
                if (html.toString().indexOf('form-group') > 0) {
                    validError(html);
                } else {
                    $("#filter-form-content").find('.alert-danger').hide();
                    $("#filter-form-content").find('.is-invalid').removeClass('is-invalid');
                    $("#filter-form-content").find('.is-valid').removeClass('is-valid');
                    $("#filter-form-content").find('.invalid-feedback').remove();
                    $("#content-block").html(html);
                    $("#content-block").find(".row").click(onRowClick);

                    $(".outer_block").hide();
                    $("#filter-block").hide();
                }
            },
            error: function (xhr, errmsg ) {
                $("#error-message").show().text("Мы не можем обработать  данные! " + errmsg);
            }
        })
    }


    function save_new_request() {
        $.ajax({
            type: "POST",
            url: "/new_request/",
            cache: false,
            data: $("#new-request-form").serialize(),
            success: (function (html) {
                if (html.toString().indexOf("Success") >= 0) {

                    $("#new-request-block").hide();
                    saveFilter(getFilterAjaxValidErrorMainForm, getFilterAjaxServerErrorMainForm);
//                   $(".outer_block").hide();
                }
                else {

                    $("#new-request-block").html(html);

                    $("#save-new-request").click(save_new_request);
                    $("#new-request__btn-close").click(close_new_request);
                }
            }),
            error: function (xhr, errmsg, err) {
                $("#new-request-error-message").text(error_text_messsage + err)
            }
        });
    }

    function close_new_request() {
        $("#new-request-block").hide();
        saveFilter(getFilterAjaxValidErrorMainForm, getFilterAjaxServerErrorMainForm);
//       $(".outer_block").hide();
    }

    function onRowClick() {

        var text = "";
        $(this).find('a').each(function () {
            text = $(this).attr('href');
        });
        if (text == "") {
        } else {
            $(".outer_block").show();

             $("#correct_request-block").find(".card-body").html("");
            $("#correct_request-block").show();
            $.ajax({
                type: "GET",
                url: text,
                cache: false,
                success: (function (html) {
                        $("#correct_request-block").html(html);
                        $("#correct-request__btn-close").click(close_correct_request);
                        $("#correct-request__save-request").click(save_correct_request_form);

                    }

                ),
                error: (function () {
                    $("#correct_request-block").find(".alert #correct-request-alert").text(error_text_messsage);
                    $("#correct_request-block").find(".close").click(close_correct_request);
                    $("#correct_reque").find(".alert").show();

                })
            });
        }
    }

    function save_correct_request_form(){
        id=$("#request-form").find("#id_request").text().trim();
        url ="/request/"+id+"/&";

        alert(id+ " "+ url);
        $.ajax({
            type:"POST",
            url :url,
            data:$( "#request-form" ).serialize(),
            cashe:false,
            success:(function (json){
                $("#request-form").find(".is-invalid").removeClass("is-invalid");
                    $("#request-form").find(".invalid-feedback").hide();
                if (json != "Success") {

                    $.each(json, function (key) {
                        var el = $("#request-form").find("[name='"+ key+"']");
                        $(el).addClass("is-invalid");
                        alert( key+" "+json[key][0].message);
                        el2=$("#request-form").find("#id_" + key+" ~ .invalid-feedback");
                        $(el2).html(json[key][0].message);
                        $(el2).show();
                        $(el2).removeClass("hidden");


                    })

                } else {
                    $("#correct_request-block").find("form-control").hasClass("is-valid")
                }
            }),
            error:(function(){
                 $("#correct_request-block").find(".alert").text(error_text_messsage);

                    $("#correct_reque").find(".alert").show();
                })

        })
    }

    function receive_correct_request(){
        p_form =$(this).parents("form").first();
        text = $( p_form).find("#cur_user").text;
        opt =$( p_form).find("#id_receive_user").find('option[value='+text+']');
        if (opt) {
            $(opt).prop('selected', true);
        }


    }

    function close_correct_request() {
        $("#correct_request-block").hide();
        saveFilter(getFilterAjaxValidErrorMainForm, getFilterAjaxServerErrorMainForm);
//       $(".outer_block").hide();
    }

    function after_filter() {
        filter_initWidjects();
    }



    after_filter();

    $("#show-filter").click(function () {
        $(".outer_block").show();
        $("#filter-block").show();
        filter_initWidjects();
    });

    $("#hide-filter").click(function () {
        $("#filter-block").hide();
        $(".outer_block").hide();
    });

    $("#save-filter").click(function () {
        saveFilter(getFilterAjaxValidErrorFilterForm, getFilterAjaxServerErrorFilterForm);
    });


    $("#new-request").click(function () {
        $(".outer_block").show();
        $.ajax({
            type: "GET",
            url: "/new_request/",
            cache: false,
            success: (function (html) {
                $("#new-request-block").html(html);
                $("#save-new-request").click(save_new_request);
                $("#new-request__btn-close").click(close_new_request);



            }),
            error: function (xhr, errmsg, err) {
                $("#new-request-block").html("<p>  " + error_text_messsage + err + "</p><div class='row'>" +
                    "<button class='btn btn-info' >Закрыть</button></div>");
                $("#new-request-block").show();
            }
        })
    });

    $("#content-block").find(".row").click(function () {
        var text = null;
        $(this).find('a').each(function () {
            text = $(this).attr('href');

        });
        if (text != null) {
            $(".outer_block").show();
            $("#correct_request-block").show();
            $.ajax({
                type: "GET",
                url: text,
                cache: false,
                success: (function (html) {
                        $("#correct_request-block").html(html);
                        $("#correct-request__btn-close").click(close_correct_request);
                        $("#correct-request__save-request").click(save_correct_request_form);
                    }

                ),
                error:(function(){
                    // language=JQuery-CSS
                    $("#correct_request-block").find(".alert #correct-request-alert").text(error_text_messsage);
                    $("#correct_request-block").find(".close").click(close_correct_request);
                    $("#correct_request").find(".alert" ).show();
                })
            });



        }


    });
});