$(document).ready(function(){
    $(".dSideText").click(function(){
        var id = $(this).data("id");
        $(" .dSideText ").removeClass(" dSideTextSelected ");
        $(this).addClass(" dSideTextSelected ");
        $(" .demo ").fadeOut(250);
        $(" .demo[data-id="+ id +"] ").fadeIn(250);
    });
});