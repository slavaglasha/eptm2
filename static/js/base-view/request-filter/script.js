$(document).ready(function() {
   // $(".wait-block").show();
    function addBlur(){
        $("#flex-container").addClass('blur');
        $(".need-blur").addClass('blur');

    }
   function closeBlur() {
        $(".blur").removeClass('blur');
       $(".wait-block").fadeOut(50);
    }

    var error_messages_lg = "Ошибка обработки  данных на сервере! ";

    $('#updateRequestModal').find('#btn_save_new').click(save_update_request);
    $('#newRequestModal').find('#btn_save_new').click(save_new_request);

    load_new_request_form(closeBlur);//загрузим форму для новой заявкисразу

     /*--init widgets --*/
   function connectUser(form){
           el = $(form).find("#id_request_outer_User");
           el.parent().parent().remove();
           $(form).find("#id_request_user").parent().append(el) ;
        }

   function searchDep(val,parent_block){
        $("#id_request_outer_department").val($(parent_block).find("#user-"+val).find(".department").text());
        $("#id_request_outer_status").val($(parent_block).find("#user-"+val).find(".position").text());


   }

  function clearDep(parent_block){
      $(parent_block).find("#id_request_outer_department").val("");
      $(parent_block).find("#id_request_outer_status").val("");
  }

  function initSelectNew(){
      $( "#id_place" ).selectmenu();
      $("#newRequestModal #id_request_user").combobox({"id_innput":"newRequestModal #id_request_outer_User",
                                                                "enabaleOther":true,
                                                                "doOnSelect":searchDep,
                                                                "doOnClear":clearDep            });

            $(".custom-combobox-input").addClass("form-control form-control-sm mr-sm-0");
            $(".custom-combobox").addClass("input-group mb-2 mb-sm-0");
            $(".custom-combobox a").addClass("input-group-addon");
  }


   function initWidgets(){

         $(".datepicker-need").datepicker({

                    todayButton:true,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii',
                    position:'bottom right'

            });
   }

  // initWidgets();
    /*--new request---*/
    function load_new_request_form(func){
         $.ajax({
               type: "get",
               cache: false,
               url: "/base/new-request/",
               success:function(htmll){
                   hhtml = $.parseHTML( htmll );

                   $('#newRequestModal').find('.modal-body').html(htmll);
                   if (func!=undefined){func();}

                   initWidgets();
                   connectUser($("#new-request-form"));
                   initSelectNew();

                   // $('#newRequestModal').find('form').show();
                  // $('#newRequestModal').find('form').addClass("form-show");

               },
               error: function (xhr, errmsg ) {

                $("#newRequestModal").find(".modal-body").text(error_messages_lg + errmsg);
                if (func!=undefined){func();}
            }
           });
    }

    function clear_new_request_form(){
        $('#newRequestModal').find("input[type='text']").value("");
        $('#newRequestModal').find("textarea").value("");
        $('#newRequestModal').find("select").value("");
        $('#newRequestModal').find("#new-request-error-message").html("");


    }


    function save_new_request(){
        if (!$(this).hasClass('btn_disabled')) {
            if ($('#newRequestModal').find("#new-request-form").find("input")) {
                $('#newRequestModal').find(".wait-block").show();

                $.ajax({
                    type: "post",
                    data: $("#new-request-form").serialize(),
                    cache: false,
                    url: '/base/new-request/',
                    success: function (html) {
                        if (html.toString().indexOf('new-request-form') > 0) {

                            $('#newRequestModal').find('.modal-body').html(html);
                            $('#newRequestModal').find('form').slideDown(10);
                            $('#newRequestModal').find(".wait-block").hide();


                        } else {
                            /*Показать сообщение о создании заявки*/

                            s = $(html);


                            $("#new-request-error-message").text($('.message_created', s).html());
                            $("#newRequestModal").find(".modal-title").text($('#number_reauest', s).html());
                            $('#newRequestModal').find(".invalid-feedback").hide();
                            $('#newRequestModal').find(".invalid-feedback").hide();
                            $('#newRequestModal').find(".is-invalid").removeClass("is_invalid").removeClass('this-invalid').addClass('is-valid').addClass('this-valid');
                            $('#newRequestModal').find("#btn_save_new").addClass("btn_disabled");
                            $("#btn_new_request_correct").show();
                            $('#newRequestModal').find(".wait-block").hide();
                            /*перезагрузка страницы ck cgbcrjb
                            $('#newRequestModal').modal('hide');
                            clear_new_request_form();*/
                            location.reload(); //перезагрузка страницы
                        }
                    },
                    error: function (xhr, errmsg) {

                        $('#newRequestModal').find("#new-request-error-message").html("error_messages_lg");

                        $('#newRequestModal').find(".wait-block").hide();

                    }


                })
            }
        }
    }
    /*--new request--*/

    /*--save updaterequest --*/
    function save_update_request(){
        if (!$(this).hasClass('btn_disabled')) {
            if ($('#updateRequestModal').find("#update-request-form").find("input")) {
                var id = $("#id").text();
                $.ajax({
                    type: "post",

                    data: $("#update-request-form").serialize(),
                    cache: false,
                    url: "/base/update-request/" + id + "/",
                    success: function (html) {
                        if (html.toString().indexOf('update-request-form') > 0) {

                            $('#updateRequestModal').find('.modal-body').html(html);
                            $('#updateRequestModal').find('form').fadeIn(10);


                        } else {
                            $('#updateRequestModal').modal('hide');
                            location.reload(); //перезагрузка страницы
                        }
                    },
                    error: function (xhr, errmsg) {

                        $("#newRequestModal").find(".modal-body").text(error_messages_lg + errmsg);

                    }
                })
            }
        }
    }
    /*--- update --*/

    if ($("#filterModal").find(".is-invalid").length>0){
        $("#filterModal").modal('show');
    }

    // language=JQuery-CSS
    $('.modal').on('show.bs.modal', function (e) {
        addBlur();

    });

    $('.modal').on('hidden.bs.modal', function (e) {
        closeBlur();
    });

    $('#newRequestModal, #updateRequestModal').on('hidden.bs.modal', function (e) {
        closeBlur();
        //$(this).find(".modal-body").html('');
        //$('.modal form').removeClass("form-show");

        //$('.wait-block').show();
       // location.reload();
    });

    $("#btn-new-request").click(function(){
        $('#newRequestModal').find("#new-request-error-message").html("");
        $("#newRequestModal").modal('show');

    });

    $('#content-block').find('.row').click(function(){
        if ($(this).find('a')){
            var id = $(this).find('a').text();
            var number = $(this).find('.number-column').text();

            $("#updateRequestModal").modal('toggle').find('#updateRequestModal').text("Заявка №" + number);
            $.ajax({
                type: "get",
                cashe: false,
                url: "/base/update-request/" + id + "/",
                success: function (html) {
                    $("#updateRequestModal .modal-body").html(html);
                    $('#updateRequestModal').find('form').slideDown(1000);
                    show_departure();


                },
                error: function (xhr, errmsg) {
                    $("#updateRequestModal .modal-body").text(error_messages_lg + errmsg);
                }
            })
        }
    });





}


);