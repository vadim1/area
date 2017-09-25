$(document).ready(function () {
    $(".start").delay(1000).fadeTo("slow", 1.0);
    $(".start2").delay(2000).fadeTo("slow", 1.0);
});

function nextbtn() {
    var first_hidden = $('#list').find('li:hidden').first();
    first_hidden.show();
    if ($('#list').find('li:hidden').length) {
        // There are more hidden items
        $('#and').appendTo(first_hidden);
    } else {
        $('#and').hide();
    }
    return false;
}
