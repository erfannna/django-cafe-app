var pId;
$(" .TempsList ").click(function(e) {
    e.preventDefault();
    $(" .TempsList ").removeClass(" TempsListActive ");
    $(this).toggleClass(" TempsListActive ");
    pId = $(this).data('id');
    $(" #submit ").show(150);
});
$(" #submit ").click(function(e) {
    e.preventDefault();
    window.location.replace('/pay/request/subscription/'+ pId);
});