function connectUser(form){
           el = $(form).find("#id_request_outer_User");
           el.parent().parent().remove();
           $(form).find("#id_request_user").parent().append(el) ;
        }

function connectPlace(form){
           el = $(form).find(" #id_place_outer");
           el.parent().parent().remove();
           $(form).find("#id_place").parent().append(el) ;
        }
