$(document).ready(function() {

    if ($("#exampleModal .is-invalid").length>0){

        $("#exampleModal").modal('show');
    }

    $('.modal').on('show.bs.modal', function (e) {
        $("#flex-container").addClass('blur');

    })

    $('.modal').on('hidden.bs.modal', function (e) {
        $("#flex-container").removeClass('blur');
    })

    $("#btn-new-request").click(function(){
        $("#newRequestModal").modal('toggle');
    })
}
);