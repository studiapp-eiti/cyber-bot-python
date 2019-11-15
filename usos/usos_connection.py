import rauth
import os


class USOSConnection:
    """Class used to setup connection with USOS API"""

    # Environment variables names
    CONSUMER_KEY_VARNAME = 'USOS_KEY'
    CONSUMER_SECRET_VARNAME = 'USOS_SECRET'

    def __init__(self):
        """Get USOS API key and secret from system environment and store them in private fields"""
        if USOSConnection.CONSUMER_KEY_VARNAME not in os.environ.keys() \
                or USOSConnection.CONSUMER_SECRET_VARNAME not in os.environ.keys():
            raise OSError('USOS API client key and secret not set in system environment')

        self._consumer_key = os.getenv(USOSConnection.CONSUMER_KEY_VARNAME)
        self._consumer_secret = os.getenv(USOSConnection.CONSUMER_SECRET_VARNAME)

    def get_user_oauth_session(self, usos_token, usos_token_secret):
        """Returns session for user identified with usos_token and usos_token_secret args"""
        return rauth.OAuth1Session(self._consumer_key, self._consumer_secret, usos_token, usos_token_secret)
