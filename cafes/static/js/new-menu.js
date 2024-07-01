$(" .cPros ").click(function(e) {
    e.preventDefault();
    $(this).toggleClass(" cProsSelected ");
});
$(" .tPreview ").click(function(e) {
    e.preventDefault();
    $(" .tPreview ").removeClass(" tThumbnailSelected ");
    $(" .tPreview ").css('filter', 'grayscale(.5)');
    $(this).toggleClass(" tThumbnailSelected ");
});
$(" #submit ").click(function(e) {
    e.preventDefault();
    $(this).hide();
    $(" #loading ").fadeIn(150);
    let pros = [];
    $(" .cProsSelected ").each(function() {
        pros.push( $(this).data('id') );
    });
    $.post('/menu/new',
      {
        'templateId': $(" .tThumbnailSelected ").data('id'),
        'prosList[]': pros
      },
      function(data){
        if (data['status'] == 'ok')
        {
            $(" #qrDown ").attr("href", data['qr']);
            $(" #nMenuQr ").attr("src", data['qr']);
            let url = 'https://barisca.ir'+ data["url"] +'';
            $(" #menuUrl ").text(url);
            $(" .popUpBg ").css('display', 'flex');
            $(" #success ").css('display', 'flex');
            $(" #loading ").hide();
            $(" #submit ").fadeIn(150);
        }
      }
    );
});
$(" #urlCopy ").click(function(e) {
    e.preventDefault();
    let url = $(" #menuUrl ").text();
    navigator.clipboard.writeText(url);
    alert("لینک منو کپی شد !");
});
$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #success ").fadeOut(200);
});