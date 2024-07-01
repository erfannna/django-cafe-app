$(" #nProductPhoto ").change(function(input){
    var file = $(this).get(0).files[0];

    if(file){
        var reader = new FileReader();

        reader.onload = function(){
            $("#pPhotoPre").attr("src", reader.result);
            $("#pPhotoPre").show();
            $(".deletePic").show();
            $("#pPhotoIco").hide();
        }
        reader.readAsDataURL(file);
    }
});
$(document).on('click', '#choosePic', function(event) {
    event.preventDefault();
    $(" #nProductPhoto ").click();
});
$(" .deletePic ").click(function(e) {
    e.preventDefault();
    $(" #pPhotoPre ").attr("src", "");
    $(" #nProductPhoto ").val("");
    $("#pPhotoIco").show();
    $("#pPhotoPre").hide();
    $(this).hide();
});

var pId;
$(" #mForm ").submit(function(e) {
    e.preventDefault();
    $(" #submit ").hide();
    $(" #loading ").show();
    let data = new FormData(this);
    fetch("/product/new", {
        method: 'POST',
        body: data,
    }).then(response => response.json()).then(data => {
        var id = data['id'];
        var name = data['name'];
        var price = data['price'];
        var cat = data['cat'];
        var img = data['img'];
        let cat_status = $(' .cProsCat[data-id="'+ cat +'"] ').length;
        if (cat_status == 0){
            $(" #cProsList ").prepend('<span class="cProsCat" data-id="'+ cat +'">'+ cat +'</span>');
        };
        if (img) {
            $(' .cProsCat[data-id="'+ cat +'"] ').after('<div class="proInfo" data-id="'+ id +'"><img class="proPhoto" src="'+ img +'" alt=""><span class="cPros" data-id="'+ id +'">'+ name +'</span><span class="proPrice">'+ price.toLocaleString("en-US") +' ت</span><a href="/product/'+ id +'/update"><span class="editBtn fi-rr-edit"></span></a><span class="editBtn deleteBtn fi-rr-cross-small" data-id="'+ id +'" data-title="'+ name +'"></span></div>');
        } else {
            $(' .cProsCat[data-id="'+ cat +'"] ').after('<div class="proInfo" data-id="'+ id +'"><span class="proPhotoIco fi-rr-coffee-pot"></span><span class="cPros" data-id="'+ id +'">'+ name +'</span><span class="proPrice">'+ price.toLocaleString("en-US") +' ت</span><a href="/product/'+ id +'/update"><span class="editBtn fi-rr-edit"></span></a><span class="editBtn deleteBtn fi-rr-cross-small" data-id="'+ id +'" data-title="'+ name +'"></span></div>');
        }
        $(" .add_popUpBg ").css('display', 'flex');
        $(" #add_success ").fadeIn(200);
        $(" #loading ").hide();
        $(" #submit ").show();
    }).catch(error => {
        $(" #loading ").hide();
        $(" #error ").show(150);
        $(" #submit ").show();
    });
});

$(" #cProsList ").on("click", ".deleteBtn", function(e) {
    e.preventDefault();
    $(" #delPro ").text($(this).data('title'));
    pId = $(this).data('id');
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
$(" #add_Close ").click(function(e) {
    e.preventDefault();
    $(" .add_popUpBg ").fadeOut(150);
    $(" #add_success ").fadeOut(200);
});
$(" #delY ").click(function(e) {
    e.preventDefault();
    $.post('/product/delete',
      {
        'id': pId,
      },
      function(data){
        if (data['status'] == 'ok')
        {
            $(' .proInfo[data-id="'+ pId +'"] ').fadeOut(300);
            $(" #confirm ").fadeOut(200);
            $(" #success ").fadeIn(200);
        }
      }
    );
});