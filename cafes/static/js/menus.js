let mId;
$(" .mDel ").click(function(e) {
    e.preventDefault();
    $(" #delPro ").text($(this).data('title'));
    mId = $(this).data('id');
    $(" .popUpBg ").css('display', 'flex');
    $(" #confirm ").fadeIn(200);
});
$(" #delN ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #confirm ").fadeOut(200);
});
$(" #aClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #success ").fadeOut(200);
});
$(" #delY ").click(function(e) {
    e.preventDefault();
    $.post('/menu/delete',
      {
        id: mId,
      },
      function(data){
        if (data['status'] == 'ok')
        {
            $(' .TempsList[data-id="'+ mId +'"] ').fadeOut(300);
            $(" #confirm ").fadeOut(200);
            $(" #success ").fadeIn(200);
        }
      }
    );
});

$(" .setDefault ").click(function(e) {
    e.preventDefault();
    var m_id = $(this).data('id');
    $.post('/menu/default',
      {
        id: m_id,
      },
      function(data){
        if (data['status'] == 'ok')
        {
            var preDefault = $(' #isDefault ').data('id');
            $(' #isDefault ').remove();
            $('<span id="isDefault" data-id="' + m_id + '" class="cProsCat" style="background-color: #b86e6e;">پیشفرض</span>').insertAfter(' .cProsCat[data-id="'+ m_id +'"] ');
            $(' .setDefault[data-id="'+ m_id +'"] ').hide();
            $(' .setDefault[data-id="'+ preDefault +'"] ').show(100);
            $(" .popUpBg ").fadeIn(200);
            $(" #defSuccess ").fadeIn(200);
        }
      }
    );
});

$(" #dClose ").click(function(e) {
    e.preventDefault();
    $(" .popUpBg ").fadeOut(150);
    $(" #defSuccess ").fadeOut(200);
});