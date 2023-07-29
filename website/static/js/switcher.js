
/*======================================================================
 Table of Content:
 
 01. Style Switcher Toggle
 
 ========================================================================*/

(function ($) {
    // Start of use strict
    'use strict';

    /*--------------------------------
     01. Color Layout Switcher
     ----------------------------------*/
    $(".switcher-trigger").click(function () {
        $(".switcher-wrapper").toggleClass("open");
    });

    $(".color-list .green button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/default.css");
        $(".color-list li.green button").css("font-size", "15px");
        $(".pink button,.blue button,.purple button,.orange button,.yellow button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .pink button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/pink.css");
        $(".color-list li.pink button").css("font-size", "15px");
        $(".green button,.blue button,.purple button,.orange button,.yellow button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .blue button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/blue.css");
        $(".color-list li.blue button").css("font-size", "15px");
        $(".green button,.pink button,.purple button,.orange button,.yellow button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .purple button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/purple.css");
        $(".color-list li.purple button").css("font-size", "15px");
        $(".green button,.pink button,.blue button,.orange button,.yellow button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .orange button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/orange.css");
        $(".color-list li.orange button").css("font-size", "15px");
        $(".green button,.pink button,.blue button,.purple button,.yellow button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .yellow button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/yellow.css");
        $(".color-list li.yellow button").css("font-size", "15px");
        $(".green button,.pink button,.blue button,.purple button,.orange button,.magenta button,.red button").css("font-size", "0px");
    });

    $(".color-list .magenta button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/magenta.css");
        $(".color-list li.magenta button").css("font-size", "15px");
        $(".green button,.pink button,.blue button,.purple button,.orange button,.yellow button,.red button").css("font-size", "0px");
    });

    $(".color-list .red button").click(function () {
        $("#optional-color").attr("href", "assets/css/color/red.css");
        $(".color-list li.red button").css("font-size", "15px");
        $(".green button,.pink button,.blue button,.purple button,.orange button,.yellow button,.magenta button").css("font-size", "0px");
    });

})(jQuery);

