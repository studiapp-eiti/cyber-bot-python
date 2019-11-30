import os
import rauth


def api_req(req):
    def catch_errors(*args, **kwargs):
        r = req(*args, **kwargs)
        if r.status_code == 400:
            raise RuntimeError('HTTP 400 Bad Request for: {}\nResponse message: {}'.format(r.url, r.json()['message']))
        elif r.status_code == 401:
            raise RuntimeError('HTTP 401 Unauthorized for: {}\nResponse message: {}'.format(r.url, r.json()['message']))
        elif r.status_code == 500:
            raise RuntimeError('HTTP 500 Internal Server Error for: {}\nResponse: {}'.format(r.url, r.text))
        return r
    return catch_errors


class User:
    """Class for holding student information required to interact with USOS API"""

    # Environment variable names
    CONSUMER_KEY_VARNAME = 'USOS_KEY'
    CONSUMER_SECRET_VARNAME = 'USOS_SECRET'

    # Class variables - shared by all users
    _consumer_key = None
    _consumer_secret = None

    def __init__(self, fb_first_name, fb_last_name, nickname, gender, usos_id,
                 usos_first_name, usos_last_name, usos_token, usos_token_secret,
                 usos_courses, locale, is_registered):
        """Constructs new User object.

        Check for environment variables is issued before attempt to get user OAuth session
        """
        self.fb_first_name = fb_first_name
        self.fb_last_name = fb_last_name
        self.usos_first_name = usos_first_name
        self.usos_last_name = usos_last_name
        self.nickname = nickname
        self.gender = gender
        self.usos_id = usos_id
        self.courses = usos_courses
        self.locale = locale
        self.is_registered = is_registered

        self._user_token = usos_token
        self._user_secret = usos_token_secret
        self.session = None

        if User._consumer_key is None or User._consumer_secret is None:
            raise ValueError('Consumer key and secret set to None. Run User.get_usos_api_key() first.')
        if self._user_token is None or self._user_secret is None:
            raise ValueError('Missing user_token and/or user_secret.')
        if self.locale not in ['pl', 'en']:
            raise ValueError('Unsupported locale: {}. Only \'pl\' or \'en\' are allowed.'.format(self.locale))

        self.session = rauth.OAuth1Session(
            User._consumer_key, User._consumer_secret,
            self._user_token, self._user_secret
        )

    def __del__(self):
        """Close session when deleting object"""
        if self.session:
            self.session.close()

    @classmethod
    def get_usos_api_key(cls):
        """Gets USOS API consumer key and secret and sets proper class variables"""
        if cls.CONSUMER_KEY_VARNAME not in os.environ.keys() \
                or cls.CONSUMER_SECRET_VARNAME not in os.environ.keys():
            raise OSError('USOS API consumer key and secret variables not found in system environment.')

        cls._consumer_key = os.getenv(cls.CONSUMER_KEY_VARNAME)
        cls._consumer_secret = os.getenv(cls.CONSUMER_SECRET_VARNAME)

    @api_req
    def api_post(self, url, *args, **kwargs):
        """Wrapper aroud session.post()"""
        return self.session.post(url, *args, **kwargs)

    @api_req
    def api_get(self, url, **kwargs):
        """Wrapper aroud session.get()"""
        return self.session.get(url, **kwargs)
