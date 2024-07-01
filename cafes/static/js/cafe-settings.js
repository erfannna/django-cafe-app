$(" #cafePhoto ").change(function(input){
    var file = $("input[id=cafePhoto]").get(0).files[0];

    if(file){
        var reader = new FileReader();

        reader.onload = function(){
            $("#pPhotoPre").attr("src", reader.result);
            $("#pPhotoPre").show();
            $("#proBox").hide();
            $("#deletePhoto").show();
            $(" #cps ").val(1);
        }
        reader.readAsDataURL(file);
    }
});
$(" #cBackPhoto ").change(function(input){
    var file = $("input[id=cBackPhoto]").get(0).files[0];

    if(file){
        var reader = new FileReader();

        reader.onload = function(){
            $("#pBackPre").attr("src", reader.result);
            $("#pBackPre").show();
            $("#pBackBox").hide();
            $("#deleteBackground").show();
            $(" #cbs ").val(1);
        }
        reader.readAsDataURL(file);
    }
});
$(document).on('click', '#pPBtn', function(event) {
    event.preventDefault();
    $(" #cafePhoto ").click();
});
$(document).on('click', '#pBBtn', function(event) {
    event.preventDefault();
    $(" #cBackPhoto ").click();
});
$(" #deletePhoto ").click(function(e) {
    e.preventDefault();
    $(" #pPhotoPre ").attr("src", "");
    $(" #cafePhoto ").val("");
    $("#pPhotoPre").hide();
    $("#proBox").show();
    $(" #cps ").val(0);
    $(this).hide();
});
$(" #deleteBackground ").click(function(e) {
    e.preventDefault();
    $(" #pBackPre ").attr("src", "");
    $(" #cBackPhoto ").val("");
    $("#pBackPre").hide();
    $("#pBackBox").show();
    $(" #cbs ").val(0);
    $(this).hide();
});
$(" #link-btn ").click(function(e) {
    e.preventDefault();
    let url = $(" #p-link ").text();
    navigator.clipboard.writeText(url);
    alert("لینک پروفایل کپی شد !");
});
$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #success ").fadeOut(200);
});