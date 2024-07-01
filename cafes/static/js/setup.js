$(' .nForm ').keyup(function(e) {
    event.preventDefault();
    var changed = $(this).val();

    if (changed != "") {
        $('.next').css("display", "flex");
    } else {
        $('.next').hide();
    }
});
$(' .next ').click(function(e) {
    var id = $(this).data('id') + 1;
    $(this).data('id', id);
    $('.next').hide();
    if (id == 3) {
        $('.backEffect').animate({ "height": "80px", "top": "345px" }, "slow" );
        $('.next').css("visibility", "hidden");
        $('#submit').css("z-index", "1");
    } else {
        $('.next').css("top", "+=244px");
        $('.backEffect').animate({ "height": "240px", "top": "100px" }, "slow" );
    }
    $('.fields').css("z-index", "0");
    $(" .fields[data-id="+ id +"] ").css("z-index", "1");
});
$(" #mForm ").submit(function(e) {
    e.preventDefault();
    $(" #submit ").hide();
    $(" #loading ").show();
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: "/configure",
        data: serializedData,
        success: function(response) {
            $(" #loading ").hide();
            $(" .popUpBg ").fadeIn(200);
            $(" #message ").css("display", "flex");
            $(" #successIcon ").css("display", "flex");
            $(" #success ").show(150);
            $(" #aClose ").show(150);
        },
        error: function(response){
            $(" #loading ").hide();
            $(" .popUpBg ").fadeIn(200);
            $(" #message ").css("display", "flex");
            $(" #errorIcon ").css("display", "flex");
            $(" #error ").show(150);
        }
    });
});