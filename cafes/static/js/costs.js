$('#costsList').on("click", ".downBtn", function(e) {
    var id = $(this).data('id');
    $(" .oTempsList[data-id="+ id +"] ").css("z-index", 1)
    $(" #delBg ").fadeIn(130);
    $(" #confirm ").show(100);
    $(" #delY ").click(function(e) {
        $(" #loading ").show(100);
        $.post('/cost/delete',
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