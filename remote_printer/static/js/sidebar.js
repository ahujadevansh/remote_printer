$(document).ready(function ($) {

    if($(window).width() > 800) {
        $(".page-wrapper").addClass("toggled");
        $("#show-sidebar").hide();
    }
    else {
        $("#close-sidebar").hide();
    }

    $(".sidebar-dropdown > a").click(function() {
    $(".sidebar-submenu").slideUp(200);
    if (
        $(this)
        .parent()
        .hasClass("active")
    ) {
        $(".sidebar-dropdown").removeClass("active");
        $(this)
        .parent()
        .removeClass("active");
    } else {
        $(".sidebar-dropdown").removeClass("active");
        $(this)
        .next(".sidebar-submenu")
        .slideDown(200);
        $(this)
        .parent()
        .addClass("active");
    }
    });

    $("#close-sidebar").click(function() {
        $(".page-wrapper").removeClass("toggled");
        $("#close-sidebar").hide();
        $("#show-sidebar").show();
    });

    $("#show-sidebar").click(function() {
        $(".page-wrapper").addClass("toggled");
        $("#close-sidebar").show();
        $("#show-sidebar").hide();
    });

});
