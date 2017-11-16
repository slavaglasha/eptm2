$(document).ready(function(){
    $("#save-new-request").click(function(){

        $.ajax({
            type:"POST",
            url:"/new_request/",
            data:$("#new-request-form"),
            success:(function(html){
                $("#new-request-block").html(html);
            }),
            error:function(xhr,errmsg,err){
                $("#new-request-error-message").text(error_text_messsage+err)
            }
        })
    });
});