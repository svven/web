// Handle popover context menu
$('[data-toggle="popover"]').popover({
    content: function() {
        var context = $('.context').clone();
        context.removeClass('menu pull-right enable-lg');
        return context;
    }
});

$(function() {
  $(window).hashchange(function() {
    var item = location.hash;
    var context = $('.context');
    $(context).children().removeClass('active');
    $(context).find('li:has(>a[href="' + item +'"])').addClass('active');
    $('[data-toggle="popover"]').popover('hide');
  });
  $(window).hashchange();
});
