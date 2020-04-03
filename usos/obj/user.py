import rauth
import usos.api


class User:
    """Class for holding student information required to interact with USOS API"""

    def __init__(self, **kwargs):
        """Initialize class members and obtain Oauth1 session for the user"""
        self.id = kwargs['id']
        self.fb_first_name = kwargs['fb_first_name']
        self.fb_last_name = kwargs['fb_last_name']
        self.usos_first_name = kwargs['usos_first_name']
        self.usos_last_name = kwargs['usos_last_name']
        self.nickname = kwargs['nickname']
        self.gender = kwargs['gender']
        self.usos_id = kwargs['usos_id']
        self.courses = kwargs['usos_courses']
        self.subscriptions = kwargs['subscriptions'].split(';')
        self.locale = kwargs['locale']
        self.is_registered = kwargs['is_registered']

        self._user_token = kwargs['usos_token']
        self._user_secret = kwargs['usos_token_secret']
        self.session = None

        if self.locale not in ['pl', 'en']:
            raise ValueError('Unsupported locale: {}. Only \'pl\' or \'en\' are allowed.'.format(self.locale))

        self.session = rauth.OAuth1Session(
            usos.api.UsosApi.get_consumer().consumer_key, usos.api.UsosApi.get_consumer().consumer_secret,
            self._user_token, self._user_secret
        )

    def __del__(self):
        """Close session when deleting object"""
        if self.session:
            self.session.close()
