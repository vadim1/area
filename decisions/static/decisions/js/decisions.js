$(document).ready(function () {
    $(".start").delay(1000).fadeTo("slow", 1.0);
    $(".start2").delay(2000).fadeTo("slow", 1.0);
    if (typeof validate === "function") {
        $('form').submit(validate);
    } else {
        $('#next').click(function () {
            var next = $(this).find('a').attr('href');
            window.location.href = next;
        });
    }
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
