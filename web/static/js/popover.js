// Handle popover context menu
$('#menu').popover({
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
    $('#menu').popover('hide');
  });
  $(window).hashchange();
});

// Create Tweets
$(".status").popover({
  content: function() {
    var anchor = $(this)[0];
    var tweetId = String($(this).data("tweet-id"));
    var target = document.createElement("div");
    target.style.width = "245px";
    twttr.widgets.createTweet(tweetId, target, {
        width: "250",
        cards: "hidden", 
        conversation: "none"
      })
    .then(function(el) {
      var doc = el.contentDocument;
      doc.querySelector(".EmbeddedTweet").style.border = "0";
      doc.querySelector(".EmbeddedTweet-tweet").style.padding = "0";
    });
    return target;
  }
});

// Dismiss popver on outside click
$('body').on('click', function(e) {
  $('[data-toggle="popover"]').each(function () {
    //the 'is' for buttons that trigger popups
    //the 'has' for icons within a button that triggers a popup
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 
      && $('.popover').has(e.target).length === 0) {
      $(this).popover('hide');
    }
  });
});