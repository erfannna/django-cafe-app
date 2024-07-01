$(" .downBtn ").click(function(e) {
    $(" .popUpBg ").fadeIn(100);
    $(" .popUpBg ").css('display', 'flex');
    $(" #newReport ").fadeIn(100);
    $(" #newReport ").css('display', 'flex');
});

$(" #mForm ").submit(function(e) {
    e.preventDefault();
    $(" #submit ").hide();
    $(" #loading ").show();
    $(" #aClose ").hide(200);
    var serializedData = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: "/reports/new",
        data: serializedData,
        success: function(response) {
            $(" #loading ").hide();
            $(" #success ").show(150);
            $(" #downRep ").attr("href", response["reportFile"]);
            $(" #downRep ").show(150);
            $(" #aClose ").show(150);
        },
        error: function(response){
            $(" #loading ").hide();
            $(" #error ").show(150);
        }
    });
});

$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" #mForm ").trigger('reset');
    $(" .popUpBg ").fadeOut(100);
    $(" #newReport ").fadeOut(100);
    $(" #success ").hide();
    $(" #error ").hide();
    $(" #downRep ").hide();
    $(" #submit ").show();
});

var page = 1;
var empty_page = false;
var block_request = false;

$(window).scroll(function() {
    var margin = $(document).height() - $(window).height() - 200;
    if  ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
        block_request = true;
        page += 1;
        $.get('?page=' + page, function(data) {
            if(data == '') {
                empty_page = true;
            }
            else {
                $(" #preload ").append(data);
                let orders = $(" #preload ").children(" .orderList ");
                $(" #loaded ").children(" .orderList ").append(orders);
                $(" #preload ").children(" .orderList ").remove();
                let reserved = $(" #preload ").children(" .reservesList ");
                $(" #loaded ").children(" .reservesList ").append(reserved);
                $(" #preload ").children(" .reservesList ").remove();
                let costs = $(" #preload ").children(" .costsList ");
                $(" #loaded ").children(" .costsList ").append(costs);
                $(" #preload ").children(" .costsList ").remove();
                let reports = $(" #preload ").children(" .xlsxList ");
                $(" #loaded ").children(" .xlsxList ").append(reports);
                $(" #preload ").children(" .xlsxList ").remove();
                block_request = false;
            }
        });
    }
});