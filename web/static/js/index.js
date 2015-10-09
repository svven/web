/*
 * Menu
 * --------------------------------------------------
*/
// Handle popover context menu
$('#burger').popover();

$(document).ready(function(){
  // Sticky nav
  $('#nav').sticky({
    topSpacing: 50 /*#header height*/
  });

  $('#nav .menu').on('click', 'li', function(e) {
    var loc = $(this).find("a").attr('href');
    window.location = loc;
  });

  // Underline selected
  $(window).hashchange(function() {
    var item = location.hash;
    var $menu = $('#nav .menu');
    if (item) {
      $menu.children().removeClass('active');
      $menu.find('li:has(>a[href="' + item +'"])').addClass('active');
    }
    else {
      $menu.children().first().addClass('active');
    }
  });
  $(window).hashchange();
});

/*
 * Twitter
 * --------------------------------------------------
 * https://dev.twitter.com/web/javascript/loading
*/
window.twttr = (function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
  if (d.getElementById(id)) return t;
  js = d.createElement(s);
  js.id = id;
  js.src = "https://platform.twitter.com/widgets.js";
  fjs.parentNode.insertBefore(js, fjs);
  t._e = [];
  t.ready = function(f) {
    t._e.push(f);
  };
  return t;
}(document, "script", "twitter-wjs"));

// Show tweets in popover
$('.tweet').each(function() {
  var $tweet = $(this);
  $tweet.popover({
    html: true, animation: false, trigger: 'hover', placement: 'bottom',
    container: $tweet, content: function() {
      var tweetId = String($(this).data('tweet-id'));
      var $target = $('<div>');
      $target.css('width', '245px');
      twttr.widgets.createTweet(tweetId, $target[0], {
          width: '250', cards: 'hidden', conversation: 'none'
        })
        .then(function(content) {
          if (typeof content !== 'undefined') {
            var $content = $(content);
            var $doc = $(content.contentDocument);
            $doc.find('.EmbeddedTweet').css('border', '0');
            $doc.find('.EmbeddedTweet-tweet').css('padding', '0');
            $content.parents('.popover').css('visibility', 'visible');
          }
        });
      return $target;
    }
  });
  $tweet.on('hide.bs.popover', function () {
    $tweet.find('.popover').css('visibility', 'hidden');
  });
});

// Dismiss tweets popovers
var $body = $('body'), 
    tap = (Tap != undefined) ? new Tap($body[0]) : null;
$body.on('tap', function(e) {
  $('[data-toggle="popover"]').each(function () {
    //the 'is' for buttons that trigger popups
    //the 'has' for icons within a button that triggers a popup
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 
      && $('.popover').has(e.target).length === 0) {
      $(this).popover('hide');
    }
  });
});

// Widget events
twttr.ready(
  function (twttr) {
    // Tweeted
    twttr.events.bind('tweet',
      function (event) {
        // alert('Tweeted.');
      }
    );

    // Followed
    twttr.events.bind('follow',
      function (event) {
        var followedUserId = event.data.user_id;
        var followedScreenName = event.data.screen_name;
        // alert('Followed ' + followedScreenName + '.');
      }
    );
  }
);

/*
 * Images
 * --------------------------------------------------
*/
// Replace all SVG images with inline SVG
var svgCache = {};
function loadSVG(url, callback, cache) {
  if (!cache[url]) {
    cache[url] = $.get(url).promise();
  }
  cache[url].done(callback);
}

$('img.svg').each(function() {
  var $img = $(this);
  var imgID = $img.attr('id');
  var imgClass = $img.attr('class');
  var imgURL = $img.attr('src');
  loadSVG(imgURL, function(data) {
    var $svg = $(data).find('svg').clone();
    if(typeof imgID !== 'undefined') {
      $svg = $svg.attr('id', imgID);
    }
    if(typeof imgClass !== 'undefined') {
      $svg = $svg.attr('class', imgClass+' replaced-svg');
    }
    $svg = $svg.removeAttr('xmlns:a');
    $svg.children().removeAttr('style');
    $img.replaceWith($svg);
  }, svgCache);
});

/*
 * Visibility
 * --------------------------------------------------
*/
// More tweets
var show = 3;

$('.tweets').each(function() {
  var $tweets = $(this);
  var tweets = $tweets.find('.tweet');
  tweets.each(function(index) {
    if (index >= show) {
      var $tweet = $(this);
      $tweet.addClass('hidden');
    }
  });
  var more = tweets.length - show;
  if (more > 0) {
    var $more = $(
      '<a class="more" href="#">' + more + ' more</a>');
    $more.click(function(e){ showMore(e.target); return false; });
    $tweets.append($more);
  }
});

function showMore(a) {
  var $more = $(a);
  $more.prevAll('.tweet').removeClass('hidden');
  $more.remove();
}

