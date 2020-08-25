/*
	Load more content with jQuery - May 21, 2013
	(c) 2013 @ElmahdiMahmoud
*/
 // $('.test1').css('display','inline');

$(function () {
    $('.test1').slice(0, 2).show();
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $('.test1:hidden').slice(0, 1).slideDown();
        if ($('.test1:hidden').length == 0) {
            $("#load").fadeOut('slow');
        }
    });
});

$('.reply-btn').on('click',function (e) {
    $('.reply-comment:hidden').show();
});

var cw = $('.ava').width();
$('.ava').css({'height':cw+'px'});

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
