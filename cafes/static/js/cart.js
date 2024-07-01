const csrftoken = Cookies.get('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
});

$(document).ready(function(){

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.action == 'addOrder'){
            $('<div class="oTempsList tableOrder" data-id="' + data.order + '"><span class="oProsCat" style="background-color: sienna;">' + data.time + '</span><span class="oProsCat" style="background-color: orangered;">مبلغ سفارش : ' + data.price.toLocaleString("en-US") + ' ت</span><br><br><span class="nName fLabel" style="font-size: 14px;">: محصولات</span><br><div id="' + data.order + '"></div></div>').insertAfter(" #todayOrders ");
        }else if(data.action == 'addProducts'){
            $(" div[id="+ data.order +"] ").append('<span class="oPros">'+ data.pName +'<span class="pNum" style="display: inline;background-color: darkred;opacity: 80%;">'+ data.pNumber +'</span></span>');
        }else if(data.action == 'delete'){
            $(" .oTempsList[data-id="+ data.id +"] ").css("z-index", 0);
            $(" .oTempsList[data-id="+ data.id +"] ").fadeOut(200);
            $(" .popUpBg ").fadeOut(150);
            $(" #confirm ").hide(100);
            $(" #deleting ").hide();
        }else if(data.action == 'closeCart'){
            $(" .tableOrder ").remove();
        }else{
            $(" #submit ").fadeIn(150);
            $(" #loading ").hide();
            block_request = false;
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    $(" #submit ").click(function(e) {
        e.preventDefault();
        let pros = [];
        $(" .cProsSelected ").each(function() {
            for(let i = 1; i <= $(this).data('num'); i++){
                pros.push( $(this).data('id') );
            }
        });
        chatSocket.send(JSON.stringify({
            'action': 'submit',
            'pros': pros,
            'table_id': tableID,
        }));
        $(" .cPros ")
        $(" #nOrderTable ").val('')
        $(" .cProsSelected ").each(function() {
            $(this).data('num', 0);
            $(this).toggleClass(" cProsSelected ");
            $(this).children(" .pNumMin ").hide();
            $(this).children(" .pNum ").hide();
        });
        $(this).hide();
        $(" #loading ").fadeIn(150);
        block_request = true;
    });

    $(" .pNumMin ").click(function(e) {
        e.preventDefault();
        let n = $(this).parent().data('num');
        if(n == 1){
            n = n - 1;
            $(this).parent().data('num', n);
            $(this).hide();
            $(this).prev().hide();
            $(this).parent().toggleClass(" cProsSelected ");
        }else{
            n = n - 1;
            $(this).parent().data('num', n);
            $(this).prev().text(n);
        }
    });

    $(" .cPro ").click(function(e) {
        e.preventDefault();

        let n = $(this).parent().data('num');
        if(n >= 1){
            n = n + 1;
            $(this).parent().data('num', n);
            $(this).next(" .pNum ").text(n);
        }else{
            n = n + 1;
            $(this).parent().data('num', n);
            $(this).parent().toggleClass(" cProsSelected ");
            $(this).next(" .pNum ").text(n);
            $(this).next(" .pNum ").show(200);
            $(this).parent().children(" .pNumMin ").show(300);
        }
    });

    $('#orderList').on("click", ".downBtn", function(e) {
        var id = $(this).data('id');
        $(" .oTempsList[data-id="+ id +"] ").css("z-index", 1)
        $(" .popUpBg ").fadeIn(130);
        $(" #confirm ").show(100);
        $(" #delY ").click(function(e) {
            chatSocket.send(JSON.stringify({
                'action': 'delete',
                'id': id,
            }));
            $(" #deleting ").show(100);
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
});