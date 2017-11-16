$(document).ready(function(){
  var error_text_messsage = "Ошибка на сервере ";

  $("#show-filter").click(function(){
    $(".outer_block").show();
    $("#filter-block").show();
  });

  $("#hide-filter").click(function(){
    $("#filter-block").hide();
    $(".outer_block").hide();
  });

  $("#save-filter").click(function(){
      $("#error-message").hide() ;
     $.ajax({
         type: "POST",
         url: "/filter_request/",
         data: $("#filter-form").serialize(),
         success:function(html) {
             if (html.toString().indexOf('form-group')>0) {
                 $("#filter-form-content").html(html)
             } else {
                 $("#content-block").html(html);
                 $(".outer_block").hide();
                 $("#filter-block").hide();
             }
         },
         error:function(xhr,errmsg,err){
           $("#error-message").show() ;
           $("#error-message").text(" Мы не можем обработать  данные! "+errmsg);
         }
     })


  });

   $("#new-request").click(function(){
       $(".outer_block").show();
       $("#new-request-block").show();

       $.ajax({
           type:"GET",
           url:"/new_request/",
           success:(function (html) {
               $("#new-request-block").html(html);
               $("#save-new-request").click(save_new_request);
           }),
           error:function(xhr,errmsg,err){
           $("#new-request-block").html("<p>  "+error_text_messsage +err+"</p><div class='row'>" +
               "<button class='btn btn-info' >Закрыть</button></div>")
         }

       })
    });


   function save_new_request() {

       $.ajax({
           type: "POST",
           url: "/new_request/",
           data: $("#new-request-form").serialize(),
           success: (function (html) {
               $("#new-request-block").html(html);
               $("#save-new-request").click(save_new_request);
           }),
           error: function (xhr, errmsg, err) {
               $("#new-request-error-message").text(error_text_messsage + err)
           }
       });
   }







});