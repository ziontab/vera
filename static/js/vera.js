$(document).ready(function() {
    $('body').on('click', '.js-event-complete', function(){
        var $btn = $(this);
        console.log($btn.data('id'));
        $.ajax({
            method: "POST",
            url: "/events/complete/",
            data: {
                id: $btn.data('id'),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            }
        })
        .done(function( msg ) {
            $btn.remove();
        });
    });
    $('body').on('click', '.js-articles-like', function(){
        var $btn = $(this);
        console.log($btn.data('id'));
        $.ajax({
            method: "POST",
            url: "/articles/like/",
            data: {
                id: $btn.data('id'),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            }
        })
        .done(function( msg ) {
             window.location = '/articles/liked/'
        });
    });
});
