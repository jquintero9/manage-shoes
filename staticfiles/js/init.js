
$(document).ready(function(){
    $(".button-collapse").sideNav();
    $("select").material_select();
    $("select[required]").css({display: "inline", height: 0, padding: 0, width: 0});
    $(".modal").modal();
});