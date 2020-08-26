/*
	Load more content with jQuery - May 21, 2013
	(c) 2013 @ElmahdiMahmoud
*/
// $('.test1').css('display','inline');

$(function () {
    $('.hidden-comment').slice(0, 2).show();
    $("#loadMore a").on('click', function (e) {
        e.preventDefault();
        $('.hidden-comment:hidden').slice(0, 2).slideDown();
        if ($('.hidden-comment:hidden').length == 0) {
            $("#load").fadeOut('slow');
        }
    });
});



$(document).ready(function () {
    $('.reply-btn').on('click', function (e) {
        var name = e.target.id
        $('.reply-comment:hidden').show();
    });
});

var cw = $('.ava').width();
$('.ava').css({ 'height': cw + 'px' });

$('a[href=#top]').click(function () {
    $('body,html').animate({
        scrollTop: 0
    }, 200);
    return false;
});

$(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
        $('.totop a').fadeIn();
    } else {
        $('.totop a').fadeOut();
    }
});
