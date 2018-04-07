// Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.
$(function () {

    if ($("input#isbn").length > 0) {
        $("input#isbn").focus();
    }

    function showProgressCircle() {
        if ($("#circle").length == 0) {
            $("label[for=isbn]").after("<div class='circle btn' id='circle' style='height: 45px !important;width: 45px !important;'>loading...</div>");
        }
    }

    function removeProgressCircle() {
        $("#circle").remove();
    }

    $("input#isbn").blur(function () {
        isbn = $(this).val();
        if (isbn.length = 13) {
            showProgressCircle();
            $.ajax({
                url: '/search_api/' + isbn,
                type: 'GET',
                dataType: 'json',
                timeout: 60000,
            }).done(function (json, textStatus, jqXHR) {
                if (json['results'] != undefined) {
                    if (json['results'][0] != undefined) {
                        if (json['results'][0]['creator'] != undefined) {
                            $("input#author").val(json['results'][0]['creator']);
                        }
                        if (json['results'][0]['publishers'] != undefined) {
                            $("input#publisher").val(json['results'][0]['publishers'][0]);
                        }
                        if (json['results'][0]['title'] != undefined) {
                            $("input#title").val(json['results'][0]['title']);
                        }
                    }
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 0) {
                    $.ajax(this);
                }
            }).always(function () {
                removeProgressCircle();
            });
        }
    });
});