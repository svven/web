window.tours = {};

/*
 * Welcome
 * --------------------------------------------------
*/
tours.welcome = new Tour({
  storage: false,
  template: function(i, step) {
    var $step = $('.step').clone();
    if (i >= 1 && i <= 3) {
      var $current = $step.find('.current');
      $current.text(i.toString() + ' of 3');
    }
    else if (i === 4) {
      var $next = $step.find('[data-role="next"]');
      $next.attr('data-role', 'end');
      $next.text('Done');
    }
    return $step.html();
  },
  onShow: function(tour, i) {
    if (i >= 1 && i <= 3) {
      step = tour.getStep(i);
      tour._showPopover(step, i);
    }
  },
  steps: [
    { // 0
      orphan: true,
      // path: '',
      title: 'Tour guide',
      content: ' \
      <p>Svven is a social news discovery tool.</p> \
      <p>It finds interesting people and content from Twitter based on what you tweet. \
      <p>Here\'s how it works in three steps.</p>',
      // backdrop: true,
      animation: false
    },
    { // 1
      path: '#tweets', 
      element: '#item-tweets', container: '#nav',
      title: 'Links you tweeted',
      content: ' \
      <p>Svven gets the links from your tweets.</p> \
      <p>It also shows other people who tweeted same links as you did lately...</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    { // 2
      path: '#fellows', 
      element: '#item-fellows', container: '#nav',
      title: 'People like you',
      content: ' \
      <p>... these people are your fellows.</p> \
      <p>Svven finds and ranks them based on the same links you tweeted.</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    { // 3
      path: '#news', 
      element: '#item-news', container: '#nav',
      title: 'Links from fellows',
      content: ' \
      <p>Your fellows also tweeted other links.</p> \
      <p>Svven aggregates and orders these links according to their ranks.</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    { // 4
      orphan: true,
      // path: '',
      title: 'That\'s it!',
      content: ' \
      <p>Keep tweeting what matters to you, \
      so Svven will give you the best of Twitter.</p> \
      <p>Run this tour anytime from the menu.</p> \
      <p>Get in touch by <a href="mailto:ducu@svven.com" target="_blank">Email</a> or \
      <a href="https://twitter.com/svvendotcom" target="_blank">Twitter</a> for details, \
      we\'re always happy to chat.</p>',
      // backdrop: true,
      animation: false
    }
  ]
});