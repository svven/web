"""
News models.
"""
from operator import attrgetter

from sqlalchemy.orm import joinedload, contains_eager

from flask import current_app
from flask.ext.login import current_user

from database.models import TwitterUser, Status
from aggregator.mixes import MixedLink, MixedReader

from aggregator.utils import timeago, munixtime

from jinja2.utils import unicode_urlencode as urlencode
from jinja2.filters import do_striptags as striptags, do_truncate as truncate

TWEET_MAX_LENGTH = 140
TWEET_SHORT_URL_LENGTH = 22

TWEET_TEXT = u'"{title}" via {via}'
TWEET = TWEET_TEXT + u' {url}'

TWEET_WEB_INTENT_URL = u'https://twitter.com/intent/tweet'
TWEET_WEB_INTENT_PARAMS = u'text={text}&url={url}&related={related}' # via into text

class WebLink(MixedLink):
    "Web Link."
    def __init__(self, **kwargs):
        "Base init."
        super(WebLink, self).__init__(**kwargs)
        # self._pickers = None

    @property
    def clean_title(self):
        return self.title and striptags(self.title) or self.site

    @property
    def tweet_url(self):
        title = self.clean_title
        url = self.url # u'http://svven.it/%s' % self.slug
        
        related = u'svvendotcom'
        via = u'@%s' % related
        ## Leave out mentions for now
        # mentions = [u'@%s' % f.screen_name for \
            # f in self.fellows if f.screen_name != current_user.screen_name][:3]
        # if mentions:
            # via += u' & %s' % u' '.join(mentions)

        title_length = TWEET_MAX_LENGTH - \
            len(TWEET.format(title='', via=via, url='')) - TWEET_SHORT_URL_LENGTH - 1
        title = truncate(title, length=title_length)
        text = TWEET_TEXT.format(title=title, via=via)

        tweet_url = u'?'.join((TWEET_WEB_INTENT_URL, TWEET_WEB_INTENT_PARAMS.format(
            text=urlencode(text), url=urlencode(url), related=urlencode(related))
        ))
        return tweet_url
    
    # @property
    # def pickers(self):
    #     "Sorted link readers."
    #     pickers = {int(picker_id): picker_moment for \
    #         picker_id, picker_moment in self.get_pickers(withscores=True)}
    #     readers = WebReader.query.filter(WebReader.id.in_(pickers.keys())).all()
    #     for reader in readers:
    #         reader.moment = pickers[reader.id]
    #     readers.sort(key=attrgetter('moment'), reverse=True)
    #     self._pickers = readers
    #     return self._pickers


class WebReader(MixedReader):
    "Web Reader."
    def __init__(self, **kwargs):
        "Base init."
        super(WebReader, self).__init__(**kwargs)
        self.init()

    def init(self):
        self._picks = None
        self._fellows = None
        self._edition = None
    
    @property
    def is_current_user(self):
        return current_user.is_authenticated() and \
            self.screen_name == current_user.screen_name
    
    @property
    def user(self):
        has_user = super(WebReader, self).user
        if has_user:
            from ..models import WebUser
            
            if not getattr(self, '_user', None):
                self._user = self.auth_user
                self._user.__class__ = WebUser
            return self._user # cached
        else:
            return None
    
    def load(self):
        "Load details from database (and Twitter!)."
        self.init()

        # Fellows
        fellows = {int(fellow_id): fellow_fellowship for \
            fellow_id, fellow_fellowship in self.get_fellows(withscores=True)}
        if fellows:
            readers = WebReader.query.filter(WebReader.id.in_(fellows.keys())).all()
            for reader in readers:
                reader.fellowship = fellows[reader.id]
            readers.sort(key=attrgetter('fellowship'), reverse=True)
        else:
            readers = []
        self._fellows = readers
        fellows = self._fellows
        fellows_dict = {f.id: f for f in fellows}
        
        # Friendships
        # TODO: Move this elsewhere and cache it
        if current_user.twitter_user:
            twitter = current_user.twitter
            user_id = current_user.twitter_user.user_id
            twitter_fellows_dict = {f.twitter_user_id: f \
                for f in [self] + fellows if f.twitter_user_id}
            user_ids = twitter_fellows_dict.keys()
            try:
                friendships = twitter.lookup_friendships(user_id=user_id, user_ids=user_ids)
                for friendship in friendships:
                    twitter_fellows_dict[friendship.id].friendship = friendship
            except Exception, e:
                current_app.logger.warning("Fail loading friendships (%s, %s)", \
                    current_user.screen_name, self.screen_name)
                current_app.logger.exception(e)

        # Picks
        picks = {int(link_id): link_moment for \
            link_id, link_moment in self.get_picks(withscores=True)}
        if picks:
            links = WebLink.query.filter(WebLink.id.in_(picks.keys())).all()
            for link in links:
                link.moment = picks[link.id]
            links.sort(key=attrgetter('moment'), reverse=True)
            for link in links:
                pickers_ids = set(int(picker_id) for picker_id in link.get_pickers())
                link_fellows = [fellows_dict[fid] for \
                    fid in pickers_ids.intersection(fellows_dict)]
                link_fellows.sort(key=attrgetter('fellowship'), reverse=True)
                link.fellows = [self] + link_fellows
                link.statuses = {}
        else:
            links = []
        self._picks = links
        picks_dict = {l.id: l for l in links}

        # Edition
        edition_fellows = self.get_edition_fellows()
        edition = {int(news_id): (news_relevance, \
            [int(fellow_id) for fellow_id in edition_fellows[news_id].split(',')]) \
            for news_id, news_relevance in self.get_edition(withscores=True)}
        if edition:
            links = WebLink.query.filter(WebLink.id.in_(edition.keys())).all()
            for link in links:
                link.relevance, link.fellows_ids = edition[link.id]
            links.sort(key=attrgetter('relevance'), reverse=True)
            for link in links:
                link_fellows = [fellows_dict[fid] for fid in link.fellows_ids]
                link_fellows.sort(key=attrgetter('fellowship'), reverse=True)
                link.fellows = link_fellows
                link.statuses = {}
        else:
            links = []
        self._edition = links
        edition_dict = {l.id: l for l in links}

        # Statuses
        link_ids = picks_dict.keys() + edition_dict.keys()
        user_ids = [self.twitter_user_id] + [f.twitter_user_id for f in fellows]
        if link_ids and user_ids:
            statuses = Status.query.with_entities(
                Status.link_id, Status.user_id, Status.status_id).filter(
                Status.link_id.in_(link_ids), Status.user_id.in_(user_ids)).all()
            for status in statuses:
                link_id, user_id, status_id = (status[0], status[1], status[2])
                link = picks_dict.get(link_id, edition_dict.get(link_id, None))
                link.statuses[user_id] = status_id

    def reload(self):
        "Should add various arguments here."
        self.set_fellows() # moment_min=None, moment_max=None, 
        # picks_count=config.PICKS_COUNT
        self.set_edition(moment_min=munixtime(timeago(hours=30))) # moment_min=None, 
        # moment_max=None, fellows_count=config.FELLOWS_COUNT, picks_count=config.PICKS_COUNT
        self.load()

    def refresh(self, session):
        "Process twitter user timeline and statuses."
        assert self.is_current_user
        from poller.twitter.job import TimelineJob

        statuses = []
        try: # process user timeline
            job = TimelineJob(
                users=[self.twitter_user], twitter=self.user.twitter)
            job.do(session)
            statuses = [s for s in job.statuses if not s.link_id]
        except Exception, e:
            session.rollback()
            current_app.logger.warning("Fail processing timeline (%s)", self.screen_name)
            current_app.logger.exception(e)
        
        # summarize new statuses
        print statuses
    
    ## Loaded properties
    @property
    def picks(self):
        "Sorted picked links."
        return self._picks

    @property
    def fellows(self):
        "Sorted fellow readers."
        return self._fellows

    @property
    def edition(self):
        "Sorted edition links."
        return self._edition


def get_reader(screen_name):
    return WebReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(WebReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
