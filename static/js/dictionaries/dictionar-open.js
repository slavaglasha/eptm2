url_open="/dictionaries/departments-list-json/";
object_name = "Ltgfhnfvtyns";
class DictionaryOpen{
    constructor(url_open, object_name) {
        this.url_open = url_open;
        this.object_name = object_name;
        this.isLoaded = false;
    }

    loadList(){
         $("#wait").fadeIn(100);
         $.ajax({
               type: "get",
               cache: false,
               url: this.url_open,

               success:function(json){
                   if (json.success) {
                       let num=0;
                       $.each(json.objects, function (key, item) {
                           let newrow = $("#first-row").clone();
                           if (item!==null) {
                               $.each(item, function (inkey, val) {
                                   $(newrow).find("." + inkey).html(val);

                               });

                           }
                           if (item!==null) {
                                num++;
                               $(newrow).find(".number").text(num);
                               $(newrow).attr('id', 'row-' + item.id).removeClass("hidden");
                               $("#main-list").append(newrow);
                               //id = item.id;
                           }


                       });



                      // setRowUpdater(); //установка собітия на строки окно просмотра заявок
                       $("#wait").fadeOut(100);

                   }else{
                        $(".wait-block").html(error_load_data + '-'+errmsg);
                         this.isLoaded= false;
                   }
               },
               error: function (xhr, errmsg ) {
                $(".wait-block").html(error_load_data + '-'+errmsg);
                this.isLoaded= false;

            }
           });
    }
}

$(document).ready(function () {

    let main_class = new DictionaryOpen(url_open, object_name).loadList();
});