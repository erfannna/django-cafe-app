let date = new Date();
let ordersNum = 0;
let cTable = 1;
let oPrice = 0;
let beep = new Audio("/static/audio/mixkit-service-bell-931.wav")

function connection() {
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
            ordersNum += 1;
            $('<div class="oTempsList" data-id="' + data.order + '"><span class="oProsCat">میز ' + data.oTable + '</span><span class="oProsCat" style="background-color: sienna;">' + data.time + '</span><span class="oProsCat" style="background-color: slateblue;">شماره سفارش :  ' + ordersNum + '</span><span class="oProsCat" style="background-color: orangered;">مبلغ سفارش : ' + data.price.toLocaleString("en-US") + ' ت</span><br><br><span class="nName fLabel" style="font-size: 14px;">: محصولات</span><br><div id="' + data.order + '"></div></div>').insertAfter(" #todayOrders ");
            cTable = data.oTable;
            oPrice = data.price;
        }else if(data.action == 'addProducts'){
            $(" div[id="+ data.order +"] ").first().append('<span class="oPros">'+ data.pName +'<span class="pNum" style="display: inline;background-color: darkred;opacity: 80%;">'+ data.pNumber +'</span></span>');
            let tPrice = data.pPrice * data.pNumber;
        }else{
            let newPrice = $(" .priceNum[data-id="+ cTable +"] ").data("num") + oPrice;
            $(" .priceNum[data-id="+ cTable +"] ").data("num", newPrice);
            $(" .priceNum[data-id="+ cTable +"] ").text(newPrice.toLocaleString("en-US"));
            beep.play();
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        $(" #onClose ").fadeIn(200);
    };
};

connection();

$(" #retry ").click(function(e) {
    connection();
    $(" #onClose ").fadeOut(200);
});

$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #success ").fadeOut(200);
});

