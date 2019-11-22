import os
import rauth


class User:
    CONSUMER_KEY_VARNAME = 'USOS_KEY'
    CONSUMER_SECRET_VARNAME = 'USOS_SECRET'
    _consumer_key = None
    _consumer_secret = None

    def __init__(self, token, secret, locale):
        self._user_token = token
        self._user_secret = secret
        self.locale = locale

        if self._consumer_key is None or self._consumer_secret is None:
            raise ValueError('Consumer key and secret set to None. Run User.get_usos_api_key() first.')

        self.session = rauth.OAuth1Session(
            self._consumer_key, self._consumer_secret,
            self._user_token, self._user_secret
        )

        self.pkt_node_ids = []

    @classmethod
    def get_usos_api_key(cls):
        if cls.CONSUMER_KEY_VARNAME not in os.environ.keys() \
                or cls.CONSUMER_SECRET_VARNAME not in os.environ.keys():
            raise OSError('USOS API consumer key and secret variables not found in system environment.')

        cls._consumer_key = os.getenv(cls.CONSUMER_KEY_VARNAME)
        cls._consumer_secret = os.getenv(cls.CONSUMER_SECRET_VARNAME)
