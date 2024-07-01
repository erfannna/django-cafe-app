$('#orderList').on("click", ".downBtn", function(e) {
    var id = $(this).data('id');
    $(" .oTempsList[data-id="+ id +"] ").css("z-index", 1)
    $(" #delBg ").fadeIn(130);
    $(" #confirm ").show(100);
    $(" #delY ").click(function(e) {
        $(" #loading ").show(100);
        $.post('/reservations/delete',
            {
                'id': id
            },
            function(data){
                if (data['status'] == 'ok')
                {
                    $(" .oTempsList[data-id="+ id +"] ").fadeOut(200);
                    $(" .oTempsList[data-id="+ id +"] ").css("z-index", 0);
                    $(" .popUpBg ").fadeOut(150);
                    $(" #confirm ").hide(100);
                    $(" #loading ").hide();
                }
            }
        );
    });
    $(" #delN ").click(function(e) {
        $(" .oTempsList[data-id="+ id +"] ").css("z-index", 0);
        $(" .popUpBg ").fadeOut(130);
        $(" #confirm ").hide(100);
    });
});

$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #success ").fadeOut(200);
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
                block_request = false;
                $(" #orderList ").append(data);
            }
        });
    }
});