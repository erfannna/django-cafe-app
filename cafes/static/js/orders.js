let date = new Date();
let cTable = 1;
let oPrice = 0;
let beep = new Audio("/static/audio/mixkit-service-bell-931.wav")

const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if(data.action == 'addOrder'){
        $('<div class="oTempsList" data-id="' + data.order + '"><span class="oProsCat">میز ' + data.oTable + '</span><span class="oProsCat" style="background-color: sienna;">' + data.time + '</span><span class="oProsCat" style="background-color: orangered;">مبلغ سفارش : ' + data.price.toLocaleString("en-US") + ' ت</span><br><br><span class="nName fLabel" style="font-size: 14px;">: محصولات</span><br><div id="' + data.order + '"></div></div>').insertAfter(" #todayOrders ");
        let tableNum = $(" .cartNum[data-id="+ data.oTable +"] ").length;
        if (tableNum == 0) {
            $(" #cartsTab ").append('<span class="cartNum " data-id="'+ data.oTable +'"> '+ data.oTable +' <small>میز</small></span>');
            $(" #cartsBox ").append('<div class="cartDetail" data-id="'+ data.oTable +'"><table class="prodsTable" data-id="'+ data.oTable +'"><caption class="cartTitle">صورتحساب</caption><tr><th colspan="4">کافه ' + cafeName + '</th></tr><tr><th colspan="2">میز شماره '+ data.oTable +'</th><th colspan="2" style="direction: ltr;">' + data.time + ' - '+ date.toLocaleDateString() +'</th></tr><tr><th>محصول</th><th>تعداد</th><th>قیمت واحد</th><th>قیمت کل</th></tr></table><div class="totalPrice"><span>قیمت کل : </span><strong><span class="priceNum" data-id="'+ data.oTable +'" data-num="0"></span> تومان</strong></div><span data-id="'+ data.oTable +'" class="closeCart cartButton">بستن صورتحساب</span><span data-id="'+ data.oTable +'" class="cartButton printCart fi-rr-print"></span></div>');
        }
        cTable = data.oTable;
        oPrice = data.price;
    }else if(data.action == 'addProducts'){
        $(" div[id="+ data.order +"] ").first().append('<span class="oPros">'+ data.pName +'<span class="pNum" style="display: inline;background-color: darkred;opacity: 80%;">'+ data.pNumber +'</span></span>');
        let tPrice = data.pPrice * data.pNumber;
        $(" .prodsTable[data-id="+ cTable +"] ").append('<tr><td>'+ data.pName +'</td><td>'+ data.pNumber +'</td><td>'+ data.pPrice.toLocaleString("en-US") +' ت</td><td>'+ tPrice.toLocaleString("en-US") +' ت</td></tr>');
    }else if(data.action == 'delete'){
        $(" .oTempsList[data-id="+ data.id +"] ").css("z-index", 0);
        $(" .oTempsList[data-id="+ data.id +"] ").fadeOut(200);
        $(" .popUpBg ").fadeOut(150);
        $(" #confirm ").hide(100);
        $(" #deleting ").hide();
    }else if(data.action == 'closeCart'){
        $(" .cartNum[data-id="+ data.cNum +"] ").remove();
        $(" .cartDetail[data-id="+ data.cNum +"] ").remove();
        let tableNums = $(" .cartNum ").length;
        if (tableNums != 0) {
            $(" .cartNum ").first().addClass(" cartNumSelected ");
            $(" .cartDetail ").first().css("display", "flex");
        }
    }else{
        let newPrice = $(" .priceNum[data-id="+ cTable +"] ").data("num") + oPrice;
        $(" .priceNum[data-id="+ cTable +"] ").data("num", newPrice);
        $(" .priceNum[data-id="+ cTable +"] ").text(newPrice.toLocaleString("en-US"));
        $(" #submit ").fadeIn(150);
        $(" #loading ").hide();
        block_request = false;
        beep.play();
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
    $(" #onClose ").fadeIn(200);
};

$(" #retry ").click(function(e) {
    location.reload();
    $(" #onClose ").fadeOut(200);
});

$('#prodSearch').keyup(function(e) {
    event.preventDefault();
    var changed = $(this).val();
    if (changed == "") {
        $(" .cPros ").show(10);
    }else{
        $(" .cPros ").each(function() {
            if ($(this).children(" .cPro ").text().indexOf(changed) >=0){
                $(this).show(10);
            }else{
                $(this).hide(10);
            }
        });
    }
});

$(" #submit ").click(function(e) {
    e.preventDefault();
    let pros = [];
    let table_id = $(" #nOrderTable ").val();
    $(" .cProsSelected ").each(function() {
        for(let i = 1; i <= $(this).data('num'); i++){
            pros.push( $(this).data('id') );
        }
    });
    chatSocket.send(JSON.stringify({
        'action': 'submit',
        'pros': pros,
        'table_id': table_id,
    }));
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
    $(" .popUpBg ").css('display', 'flex');
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

$(" #allCarts ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").css('display', 'flex');
    $(" .cartDetail ").hide();
    $(" .cartNum ").removeClass(" cartNumSelected ");
    let tableNums = $(" .cartNum ").length;
    if (tableNums != 0) {
        $(" .cartNum ").first().addClass(" cartNumSelected ");
        $(" .cartDetail ").first().css("display", "flex");
    }
    $(" #cartsBox ").css("display", "flex");
});

$(" #cClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #cartsBox ").fadeOut(200);
});

$(" #cartsTab ").on("click", ".cartNum", function(e) {
    e.preventDefault();
    let cNum = $(this).data('id');
    $(" .cartNum ").removeClass(" cartNumSelected ");
    $(this).addClass(" cartNumSelected ");
    $(" .cartDetail ").hide();
    $(" .cartDetail[data-id="+ cNum +"] ").show();
});

$(" #cartsBox ").on("click", " .printCart ", function(e) {
    e.preventDefault();
    let id = $(this).data('id');
    $(" .prodsTable[data-id="+ id +"] ").print({globalStyles: true,
                                                mediaPrint: true,
                                                title: "رسید خرید"});
});

$(" #cartsBox ").on("click", " .closeCart ", function(e) {
    e.preventDefault();
    let id = $(this).data('id');
    chatSocket.send(JSON.stringify({
        'action': 'closeCart',
        'cNum': id,
    }));
});

$(" #newCart ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").css('display', 'flex');
    $(" #newCartRedirect ").fadeIn(200);
});

$(" #ExCart ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #newCartRedirect ").fadeOut(200);
});

$(" #GoCart ").click(function(e) {
    e.preventDefault();
    var tNum = $(" #newCartNo ").val();
    if(tNum != ""){
        window.location.replace('/orders/'+ tNum);
    }
});

var page = 1;
var empty_page = false;
var block_request = false;

$(" #orderList ").scroll(function() {
    var margin = $(document).height() - $(window).height() - 50;
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
