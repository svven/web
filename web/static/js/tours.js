window.tours = {};

/*
 * Welcome
 * --------------------------------------------------
*/
tours.welcome = new Tour({
  storage: false,
  template: function(step, i) {
    return $('.step').html();
  },
  onShow: function(tour, i) {
    step = tour.getStep(i);
    tour._showPopover(step, i);
  },
  steps: [
    {
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
    {
      path: '#tweets', 
      element: '#item-tweets', container: '#nav',
      title: 'Links you tweeted',
      content: ' \
      <p>Svven gets the links from your tweets.</p> \
      <p>It also shows other people who tweeted same links as you did lately...</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    {
      path: '#fellows', 
      element: '#item-fellows', container: '#nav',
      title: 'People like you',
      content: ' \
      <p>...These people are your fellows.</p> \
      <p>Svven finds and ranks them based on the links you tweeted in common.</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    {
      path: '#news', 
      element: '#item-news', container: '#nav',
      title: 'Links from fellows',
      content: ' \
      <p>Your fellows also tweeted other links.</p> \
      <p>Svven aggregates and orders these links according to fellows\' ranks.</p>',
      // backdrop: true, backdropContainer: '#nav',
      animation: false, placement: 'bottom'
    },
    {
      orphan: true,
      // path: '',
      title: 'That\'s it',
      content: ' \
      <p>Keep tweeting what matters to you, \
      so Svven will give you the best of Twitter.</p> \
      <p>Run this tour anytime from the menu.</p> \
      <p>Get in touch by <a href="mailto:ducu@svven.com" target="_blank">Email</a> or \
      <a href="https://twitter.com/svvendotcom" target="_blank">Twitter</a> for more, \
      or if you want to help on Svven. Cheers.</p>',
      // backdrop: true,
      animation: false
    }
  ]
});