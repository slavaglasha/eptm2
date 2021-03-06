$(document).ready(function() {

    $.widget("custom.combobox", {
        _create: function () {
            this.wrapper = $("<span>")
                .addClass("custom-combobox")
                .insertAfter(this.element);
            if  (this.options.disabled){
                this.wrapper.addClass('ui-state-disabled');
            }
            this.element.hide();
            parent_block = $(this.element).parents("form").first();
            this._createAutocomplete();
            this._createShowAllButton();
            if (this.options.enabaleOther) {
                outinput = $("#" + this.options.id_innput);
                if (outinput.val() !== "") {
                    this.input.val(outinput.val());
                }
                outinput.hide();
            }else {}
            if (this.element.children(":selected")!==undefined){
                var selected = this.element.children(":selected"),
                value = selected.val() ;
                if (value!==''){}
                    this.input.val(selected.text());

            }

        },

        _createAutocomplete: function () {
            var selected = this.element.children(":selected"),
                value = selected.val() ? selected.text() : "";
            this.input = $("<input>")
                .appendTo(this.wrapper)
                .val(value)
                .attr("title", "")
                .addClass("custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left")
                .autocomplete({
                    delay: 0,
                    minLength: 0,
                    source: $.proxy(this, "_source")
                })
                .tooltip({
                    classes: {
                        "ui-tooltip": "ui-state-highlight"
                    }
                });

            this._on(this.input, {
                autocompleteselect: function (event, ui) {
                    ui.item.option.selected = true;
                    this._trigger("select", event, {
                        item: ui.item.option
                    });
                    var v = ui.item.option.value;
                    if (this.options.doOnSelect != null)
                        this.options.doOnSelect(v,$(this.element).parents("form").first());





                },

                autocompletechange: "_removeIfInvalid"
            });
        },

        _createShowAllButton: function () {
            var input = this.input,
                wasOpen = false;

            $("<a>")
                .attr("tabIndex", -1)
                .attr("title", "")
                .tooltip()
                .appendTo(this.wrapper)
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
                .addClass("custom-combobox-toggle ui-corner-right")
                .on("mousedown", function () {
                    wasOpen = input.autocomplete("widget").is(":visible");
                })
                .on("click", function () {
                    input.trigger("focus");

                    // Close if already visible
                    if (wasOpen) {
                        return;
                    }

                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete("search", "");
                });
        },

        _source: function (request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            response(this.element.children("option").map(function () {
                var text = $(this).text();
                if (this.value && ( !request.term || matcher.test(text) )) {

                    return {
                        label: text,
                        value: text,
                        option: this
                    };
                }
            }));
        },

        _removeIfInvalid: function (event, ui) {

            // Selected an item, nothing to do
            if (ui.item) {
               // alert(ui.item.option.value);
                outinput.val("");
                return;
            }

            // Search for a match (case-insensitive)
            var value = this.input.val(),
                valueLowerCase = value.toLowerCase(),
                valid = false;
            this.element.children("option").each(function () {
                if ($(this).text().toLowerCase() === valueLowerCase) {
                    this.selected = valid = true;

                    return false;
                }else{
                     this.selected = false;
                }
            });

            // Found a match, nothing to do
            if (valid) {
                outinput.val("");

                return;
            }

            // Remove invalid value
            //add another value into new fied
            if (this.options.enabaleOther) {
                if (this.options.doOnClear !== undefined){
                    this.options.doOnClear($(this.element).parents("form").first());

                }
                //this.input.val("");
                outinput.val(value);
            } else {

                this.input
                    .val("")
                    .attr("title", " Совпадений не найдено")
                    .tooltip("open");
                outinput.val("");
            }
            this.element.val("");
            this._delay(function () {
                this.input.tooltip("close").attr("title", "");
            }, 2500);
            this.input.autocomplete("instance").term = "";
        },

        _destroy: function () {
            this.wrapper.remove();
            this.element.show();
        }
    });
});

function searchDep(val,parent_block){

        $(parent_block).find("#user_department").children("option").map(function(){
                        var tv = this.value;
                        var t=$(this).text();
                        if (tv===val){
                            $(parent_block).find("#id_request_outer_department").val($(this).text());
                        }
                    });
        $(parent_block).find("#user_position").children("option").map(function(){
                        var tv = this.value;
                        var t=$(this).text();
                        if (tv===val){
                            $(parent_block).find("#id_request_outer_status").val($(this).text());
                        }
                    });
    }

function clearDep(parent_block){
    $(parent_block).find("#id_request_outer_department").val("");
    $(parent_block).find("#id_request_outer_status").val("");
}

function new_request_initWidjects(){
            $("#new-request-block").find("#id_request_user").combobox({"id_innput":"new-request-block #id_request_outer_User",
                                                                "enabaleOther":true,
                                                                "doOnSelect":searchDep,
                                                                "doOnClear":clearDep            });

            $(".custom-combobox-input").addClass("form-control form-control-sm mr-sm-0");
            $(".custom-combobox").addClass("input-group mb-2 mb-sm-0");
            $(".custom-combobox a").addClass("input-group-addon");
            $("#id_request_dateTime").datepicker({
                  // Можно выбрать тольо даты, идущие за сегодняшним днем, включая сегодня
                    todayButton:true,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii'

            })

        }

 function filter_initWidjects() {

        $("#filter-form-content #id_request_user").combobox({
            "id_innput": "filter-form-content #id_request_outer_user",
            "enabaleOther": true
        });

        $(".custom-combobox-input").addClass("form-control form-control-sm mr-sm-0");
        $(".custom-combobox").addClass("input-group mb-2 mb-sm-0");
        $(".custom-combobox a").addClass("input-group-addon");

        $(".datepicker-need").datepicker({

                    todayButton:true,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii'

            })


    }

  function filter_initWidjects2(idmain) {

        $("#"+idmain+" #id_request_user").combobox({
            "id_innput": idmain+" #id_request_outer_User",
            "enabaleOther": true
        });

        $("#"+idmain).find(".custom-combobox-input").addClass("form-control form-control-sm mr-sm-0");
        $("#"+idmain).find(".custom-combobox").addClass("input-group mb-2 mb-sm-0");
        $("#"+idmain).find(".custom-combobox a").addClass("input-group-addon");

        // $(".datepicker-need").datepicker({
        //
        //             todayButton:true,
        //             clearButton:true,
        //             timepicker: true,
        //             data_time_format: 'hh:ii'
        //
        //     });

      $(".datepicker-need").datepicker({todayButton:false,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii'});


    }


 function correct_request_initWidgets(){
       $("#correct_request-block #id_request_user").combobox({"id_innput":"correct_request-block #id_request_outer_User",
                                                                "enabaleOther":true,
                                                                "doOnSelect":searchDep,
                                                                "doOnClear":clearDep            });

            $(".custom-combobox-input").addClass("form-control form-control-sm mr-sm-0");
            $(".custom-combobox").addClass("input-group mb-2 mb-sm-0");
            $(".custom-combobox a").addClass("input-group-addon");
      $(".datepicker-need").datepicker({

                    todayButton:true,
                    clearButton:true,
                    timepicker: true,
                    data_time_format: 'hh:ii'

            })

}
