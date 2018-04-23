function correctNumber(strnumber){
    if ((strnumber.trim())!==''){
        alert(strnumber);
        var re = /^\d+$/;
        return re.test(strnumber.trim());
    }else {
        return true;
    }
}
function  converttodate(dateString){
    //match date in format DD.MM.YYYY
      var  m = /^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20\d{2}) ([0-1]\d|[2][0-3])\:([0-5][0-9])$/.exec(dateString);

    if (m) {
        $("#result").html(true);

        var parts = dateString.split(' ');
        var dstr = parts[0], tstr = parts[1];
        var dparts = dstr.split('.'), tparts = tstr.split(':');

        return new Date(dparts[2], dparts[1] - 1, dparts[0], tparts[0], tparts[1]);
    }
    else{
        return 0;
    }


}


/*проверка дат с в строках должна біть дата dd.mm.yyyy hh:mm  в первой строке дата меньше чем во второй*/
function compareDate(str1, str2) {
    var date1=0, date2=0;
    if (str1.trim()!=="") {
        date1 = converttodate(str1);
        if (date1===0) {return false;}
    }
    if (str2.trim() === '') {
    } else {
        date2 = converttodate(str2);
        if (date2 === 0) {
            return false;
        }
    }
    return !(date1 !== 0 && 0 !== date2 && date1 > date2);


}
/*проверяет правильній ввод дат для формі фильтров  eldt1, eldt2  -  input  с датой dd.mm.yyyy hh:mm*/
function checkDateIntervalElementFilter(eldt1, eldt2 ){

     //Проверка ввода дат

     if (!compareDate($(eldt1).val(),$(eldt2).val())){

         $(eldt1).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');
         $(eldt2).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');

         $(eldt2).parent().siblings('.error-text').text(correct_interval).show();
         $(eldt1).parent().parent().parent().addClass("invalid");
         return false;

     }
     else {
         $(eldt1).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         $(eldt2).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
         $(eldt2).parent().siblings('.error-text').text('').hide();
         $(eldt1).parent().parent().parent().removeClass("invalid");
         return true;
     }
 }

 function checkNumberElementFilter(eldt ){
    if (correctNumber($(eldt).val())){
       $(eldt).removeClass('is-invalid').removeClass('this-invalid').addClass('is-valid').addClass(' this-valid');
       $(eldt).parent().parent().parent().removeClass("invalid");
       $(eldt).parent().parent().siblings('.error-text').text('').hide();

       return true;
    } else{
        $(eldt).removeClass('is-valid').removeClass(' this-valid').addClass('is-invalid').addClass('this-invalid');
        $(eldt).parent().parent().parent().addClass("invalid");
        $(eldt).parent().parent().siblings('.error-text').text(correct_number).show();
        return false;
    }

 }

  function setErrortext(field, text) {
         $(field).parent().parent().parent().addClass('invalid');
            $(field).parent().siblings('.error-text').html(text);
  }

   function checkRequiredField(field ){

         if ($(field).val()===''){


            $(field).parent().parent().parent().addClass('invalid');
            $(field).parent().siblings('.error-text').html(required);
            return false;
         }else{
             $(field).parent().parent().parent().removeClass('invalid');
             return true;

         }
     }
