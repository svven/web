// Handle popover context menu
$('#menu').popover({
    content: function() {
        var $context = $('.context').clone();
        $context.removeClass('menu pull-right enable-lg');
        return $context;
    }
});

$(function() {
  $(window).hashchange(function() {
    var item = location.hash;
    var $context = $('.context');
    $context.children().removeClass('active');
    $context.find('li:has(>a[href="' + item +'"])').addClass('active');      
    $('#menu').popover('hide');
  });
  $(window).hashchange();
});

// Create Tweets
$(".tweet").each(function() {
  var $tweet = $(this);
  $tweet.popover({
    container: $tweet,
    content: function() {
      var tweetId = String($(this).data("tweet-id"));
      var $target = $("<div>");
      $target.css("width", "245px");
      twttr.widgets.createTweet(tweetId, $target[0], {
          width: "250", cards: "hidden", conversation: "none"
        })
        .then(function(content) {
          if (typeof content !== 'undefined') {
            var $content = $(content);
            var $doc = $(content.contentDocument);
            $doc.find(".EmbeddedTweet").css("border", "0");
            $doc.find(".EmbeddedTweet-tweet").css("padding", "0");
            $content.parents(".popover").css("visibility", "visible");
          }
        });
      return $target;
    }
  });
  $tweet.on('hide.bs.popover', function () {
    $tweet.find(".popover").css("visibility", "hidden");
  });
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