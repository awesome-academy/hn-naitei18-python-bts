document.getElementById("defaultOpen").click();
function openLog(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;


  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tab-content1");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tab-links");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

$(function () {
    $('.hidden-comment1').slice(0, 2).show();
    $("#loadMore1 a").on('click', function (e) {
        e.preventDefault();
        $('.hidden-comment1:hidden').slice(0, 2).slideDown();
        if ($('.hidden-comment1:hidden').length == 0) {
            $("#load").fadeOut('slow');
        }
    });
});

$(function () {
    $('.hidden-comment2').slice(0, 2).show();
    $("#loadMore2 a").on('click', function (e) {
        e.preventDefault();
        $('.hidden-comment2:hidden').slice(0, 2).slideDown();
        if ($('.hidden-comment2:hidden').length == 0) {
            $("#load").fadeOut('slow');
        }
    });
});
