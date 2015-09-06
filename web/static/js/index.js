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
 * Header
 * --------------------------------------------------
*/
// // Hide Header on on scroll down
// // https://medium.com/@mariusc23/hide-header-on-scroll-down-show-on-scroll-up-67bbaae9a78c
// var didScroll;
// var lastScrollTop = 0;
// var delta = 5;
// var headerHeight = $('#header').outerHeight();

// $(window).scroll(function(event){
//     didScroll = true;
// });

// setInterval(function() {
//     if (didScroll) {
//         hasScrolled();
//         didScroll = false;
//     }
// }, 250);

// function hasScrolled() {
//     var st = $(this).scrollTop();
//     if(Math.abs(lastScrollTop - st) <= delta)
//         return;
//     if (st > lastScrollTop && st > headerHeight){
//         // Scroll Down
//         $('#header').removeClass('noheader').addClass('noheader');
//     } else {
//         // Scroll Up
//         if(st + $(window).height() < $(document).height()) {
//             $('#header').removeClass('noheader');
//         }
//     }
//     lastScrollTop = st;
// }

/*
 * Twitter
 * --------------------------------------------------
*/
// Show tweets in popover
$('.tweet').each(function() {
  var $tweet = $(this);
  $tweet.popover({
    container: $tweet,
    content: function() {
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

/*
 * Images
 * --------------------------------------------------
*/
$('img').one('error', function() { 
  this.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
});

/*
 * Replace all SVG images with inline SVG
 */
$('img.svg').each(function() {
  var $img = $(this);
  var imgID = $img.attr('id');
  var imgClass = $img.attr('class');
  var imgURL = $img.attr('src');

  $.get(imgURL, function(data) {
    // Get the SVG tag, ignore the rest
    var $svg = $(data).find('svg');
    // Add replaced image's ID to the new SVG
    if(typeof imgID !== 'undefined') {
      $svg = $svg.attr('id', imgID);
    }
    // Add replaced image's classes to the new SVG
    if(typeof imgClass !== 'undefined') {
      $svg = $svg.attr('class', imgClass+' replaced-svg');
    }
    // Remove any invalid XML tags as per http://validator.w3.org
    $svg = $svg.removeAttr('xmlns:a');
    // Also remove style if any
    $svg.children().removeAttr('style');
    // Replace image with new SVG
    $img.replaceWith($svg);
  }, 'xml');
});
