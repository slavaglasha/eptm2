function getDateTime(str) {
    var dt = str.split(" ")[0];
    var tt = str.split(" ")[1];
    var dd =dt.split(".")[0];
    var mm=dt.split(".")[1]-1;
    var yy = dt.split(".")[2];
    var hh = tt.split(":")[0];
    var mmt = tt.split(":")[1];
    return new Date(yy,mm,dd,hh,mmt);

}
function connectUser(form){
           var el = $(form).find("#id_request_outer_User");
           el.parent().parent().remove();
           $(form).find("#id_request_user").parent().append(el) ;
        }
function connectArcticUser(form, onSearch, onClear) {
    var el = $(form).find("#id_request_outer_User");
    el.parent().parent().parent().parent().remove();
    $(el).insertAfter($(form).find("#id_request_user"));
    var attr = $(el).attr('readonly');

    var disa =  (attr && attr!==false) ;

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
    $(el).removeAttr('disabled');
    setWidgets(form);

}
function setWidgets(form){
           $(form).find("#id_number").spinner({min:0,step:1});
          // $(form).find("select:not(#id_request_user):not([multiple])").selectmenu();
           $.each($(form).find("select:not(#id_request_user):not([multiple])"), function () {
               var attr = $(this).attr('readonly');
               if (attr && attr!==false) {
                   $(this).selectmenu({disabled:true});
                   $(this).removeAttr('disabled');
               }else{
                   $(this).selectmenu();
               }
            });
           $.each($(form).find("select[multiple='multiple']"), function () {

               var attr = $(this).attr('readonly');
               if (attr && attr!==false) {
                   alert("multiple");
                   $(this).attr("disabled","");
               }
           });



           //$(form).find("select:not(#id_request_user):not([multiple])").selectmenu();
           $.each($(form).find(".datepicker-need:first-child"), function () {

                var attr = $(this).attr('readonly');
                if (attr!=undefined && attr!==false){
                    $(this).attr("disabled",'');
                } else {
                    var setd =  undefined;
                    if ($(this).attr("value")!=undefined) {
                        setdt = getDateTime($(this).attr("value"));
                         $(this).datepicker({
                        todayButton: new Date(),
                        clearButton: true,
                        timepicker: true,
                        data_time_format: 'hh:ii',
                        position: 'bottom left',
                        autoClose: true,
                        startDate:setdt,
                        needselecedtDate :setdt
                    });


                    }else {
                        $(this).datepicker({
                            todayButton: false,
                            clearButton: true,
                            timepicker: true,
                            data_time_format: 'hh:ii',
                            position: 'bottom left',
                            autoClose: true
                        });
                    }
                    //.selectDate()
                }
                // $(this).removeAttr('disabled');
           });
          $.each($(form).find(".datepicker-need:nth-child(3)"), function() {
              var attr = $(this).attr('readonly');
              $(this).datepicker({
                  todayButton: false,
                  clearButton: true,
                  timepicker: true,
                  data_time_format: 'hh:ii',
                  position: 'bottom right', autoClose: true

              });
          });
        }

function connectPlace(form){
           el = $(form).find(" #id_place_outer");
           el.parent().parent().remove();
           $(form).find("#id_place").parent().append(el) ;
        }
