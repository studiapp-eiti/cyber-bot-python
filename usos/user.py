import os
import rauth


class User:
    """Class for holding student information required to interact with USOS API"""

    # Environment variable names
    CONSUMER_KEY_VARNAME = 'USOS_KEY'
    CONSUMER_SECRET_VARNAME = 'USOS_SECRET'

    # Class variables - shared by all users
    _consumer_key = None
    _consumer_secret = None

    def __init__(self, token, secret, locale):
        """Constructs new User object.

        Check for environment variables is issued before attempt to get user OAuth session
        """
        self._user_token = token
        self._user_secret = secret
        self.locale = locale

        if User._consumer_key is None or User._consumer_secret is None:
            raise ValueError('Consumer key and secret set to None. Run User.get_usos_api_key() first.')

        self.session = rauth.OAuth1Session(
            User._consumer_key, User._consumer_secret,
            self._user_token, self._user_secret
        )

    @classmethod
    def get_usos_api_key(cls):
        """Gets USOS API consumer key and secret and sets proper class variables"""
        if cls.CONSUMER_KEY_VARNAME not in os.environ.keys() \
                or cls.CONSUMER_SECRET_VARNAME not in os.environ.keys():
            raise OSError('USOS API consumer key and secret variables not found in system environment.')

        cls._consumer_key = os.getenv(cls.CONSUMER_KEY_VARNAME)
        cls._consumer_secret = os.getenv(cls.CONSUMER_SECRET_VARNAME)
