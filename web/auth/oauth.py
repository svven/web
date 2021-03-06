"""
OAuth authentication.
http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
"""
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session

from tweepy.models import User

class OAuth(object):
    "Base authentication class."
    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_key = credentials['key']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('.oauth_callback', 
            provider_name=self.provider_name, _external=True)

    providers = None

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class TwitterAuth(OAuth):
    "Twitter authentication."
    def __init__(self):
        super(TwitterAuth, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authenticate', # instead of /authorize
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None
        oauth_session = self.service.get_auth_session(
            request_token[0], request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        user = User.parse(None, 
            oauth_session.get('account/verify_credentials.json').json())
        key = oauth_session.access_token
        secret = oauth_session.access_token_secret
        return user, key, secret


# class FacebookAuth(OAuth):
#     "Facebook authentication."
#     def __init__(self):
#         super(FacebookAuth, self).__init__('facebook')
#         self.service = OAuth2Service(
#             name='facebook',
#             client_id=self.consumer_key,
#             client_secret=self.consumer_secret,
#             authorize_url='https://graph.facebook.com/oauth/authorize',
#             access_token_url='https://graph.facebook.com/oauth/access_token',
#             base_url='https://graph.facebook.com/'
#         )
#
#     def authorize(self):
#         return redirect(self.service.get_authorize_url(
#             scope='email',
#             response_type='code',
#             redirect_uri=self.get_callback_url())
#         )
#
#     def callback(self):
#         if 'code' not in request.args:
#             return None
#         oauth_session = self.service.get_auth_session(
#             data={'code': request.args['code'],
#                   'grant_type': 'authorization_code',
#                   'redirect_uri': self.get_callback_url()}
#         )
#         user = oauth_session.get('me').json()
#         return user #, key, secret
