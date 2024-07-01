$(" #submit ").click(function(e) {
    e.preventDefault();
    let pros = [];
    let table_id = $(" #nOrderTable ").val();
    $(" .cProsSelected ").each(function() {
        for(let i = 1; i <= $(this).data('num'); i++){
            pros.push( $(this).data('id') );
        }
    });
    $.post('{% url "cafes:orders" %}',
      {
        'tableID': table_id,
        'prosList[]': pros
      },
      function(data){
        if (data['status'] == 'ok')
        {
            let id = data['oId'];
            let time = data['time'];
            let pr = data['price'];
            $(" #orderList ").prepend('<div class="oTempsList" data-id="' + id + '"><span class="oProsCat">میز ' + table_id + '</span><span class="oProsCat" style="background-color: sienna;">' + time + '</span><span class="oProsCat" style="background-color: orangered;">مبلغ سفارش : ' + pr + ' ت</span><br><br><span class="nName fLabel" style="font-size: 14px;">: محصولات</span><br><div id="' + id + '"></div></div>');
            $(" .cProsSelected ").each(function() {
                let pNumber = $(this).data('num');
                let prod = $(this).children(" .cPro ").text();
                $(" div[id="+ id +"] ").append('<span class="oPros">'+ prod +'<span class="pNum" style="display: inline;background-color: darkred;opacity: 80%;">'+ pNumber +'</span></span>');
                $(this).data('num', 0);
                $(this).toggleClass(" cProsSelected ");
                $(this).children(" .pNumMin ").hide();
                $(this).children(" .pNum ").hide();
            });
            $(" #nOrderTable ").val('');
            $(" .popUpBg ").fadeIn(130);
            $(" #success ").fadeIn(200);
        }
      }
    );
});