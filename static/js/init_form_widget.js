function connectUser(form){
           el = $(form).find("#id_request_outer_User");
           el.parent().parent().remove();
           $(form).find("#id_request_user").parent().append(el) ;
        }
function connectArcticUser(form, onSearch, onClear) {
    el = $(form).find("#id_request_outer_User");
    el.parent().parent().parent().parent().remove();
    $(el).insertAfter($(form).find("#id_request_user"));
    var disa = ($(el).attr("disabled") == 'disabled' );

    if ((onSearch === undefined) || (onClear === undefined)) {
        $(form).find("#id_request_user").combobox({
            "id_innput": $(form).attr('id') + " #id_request_outer_User",
            "enabaleOther": true,
            "disabled": disa
        });
    }
    else {
        $(form).find("#id_request_user").combobox({
            "id_innput": $(form).attr('id') + " #id_request_outer_User",
            "enabaleOther": true,
            "doOnSelect": onSearch,
            "doOnClear": onClear,
            "disabled": disa
        });
    }
    setWidgets(form);

}
function setWidgets(form){
           $(form).find("#id_number").spinner({min:0,step:1});
           $.each($(form).find("select:not(#id_request_user):not([multiple])"), function (el) {
            if ($(el).hasAttribute("readonly")){

            }
    });
           $(form).find("select:not(#id_request_user):not([multiple])").selectmenu();

           $(form).find(".datepicker-need:first-child").datepicker({todayButton:false,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii',
                                      position: 'bottom left',
               autoClose: true});
           $(form).find(".datepicker-need:nth-child(3)").datepicker({todayButton:false,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii',
                                      position: 'bottom right',autoClose: true});
        }

function connectPlace(form){
           el = $(form).find(" #id_place_outer");
           el.parent().parent().remove();
           $(form).find("#id_place").parent().append(el) ;
        }
