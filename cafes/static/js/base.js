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
    $(" .menuIcon ").click(function(e) {
        $(this).toggleClass(" menuIcon2 ");
        $(" .popUpBg ").toggle(50);
        $(" #sidebar ").toggle(50);
    });
});