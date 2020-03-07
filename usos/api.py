import os
import time
import json
import requests

from usos.obj.user import User
from usos.log import UsosLogger as logger


def _api_req(req):
    """Decorator function for catching HTTP errors during request to USOS API
    and when they occur - providing detailed information about them"""

    def request_wrapper(*args, **kwargs):
        logger.api().debug('Issuing API request...')

        retries = int(os.getenv('REQUESTS_MAX_RETRIES'))
        retry_timeout = float(os.getenv('REQUESTS_RETRY_TIMEOUT'))

        error = True
        response = None
        while error and retries != 0:
            try:
                response = req(*args, **kwargs)
                error = False
            except requests.ConnectionError as conn_err:
                logger.api().exception('Connection error occurred: %s\nRemaining retries: %d', conn_err, retries)
                time.sleep(retry_timeout)
                retries -= 1

        if response is None:
            err_msg = 'Connection retries exceeded its maximum'
            logger.api().error(err_msg)
            raise RuntimeError(err_msg)

        if response.status_code != 200:
            error_msg = 'HTTP {res.status_code} error for request: {res.url}' \
                        '\nResponse message: {res.text}'.format(res=response)

            # Note: args[1] holds User object that called this decorator (if this is not an anon API request)
            if type(args[1]) is User:
                error_msg += '\nCaller: {u.usos_first_name} {u.usos_last_name} [{u.usos_id}]'.format(u=args[1])

            error_msg += '\nRequest data:\n'
            if 'data' in kwargs.keys() and type(kwargs['data']) == dict:
                error_msg += json.dumps(kwargs['data'], ensure_ascii=False, indent=2)

            logger.api().error(error_msg)
            raise RuntimeError(error_msg)

        logger.api().debug('API request successful')
        return response

    return request_wrapper


class _UsosApiConsumer:
    """Simple class for holding consumer key and secret for USOS API Oauth1 connections"""

    # Environment variable names
    CONSUMER_KEY_VARNAME = 'USOS_KEY'
    CONSUMER_SECRET_VARNAME = 'USOS_SECRET'

    def __init__(self):
        """Gets USOS API consumer key and secret and sets proper member variables"""
        if os.getenv(_UsosApiConsumer.CONSUMER_KEY_VARNAME) is None \
                or os.getenv(_UsosApiConsumer.CONSUMER_SECRET_VARNAME) is None:
            err_msg = 'USOS API consumer key and secret variables not found in system environment.'
            logger.api().critical(err_msg)
            raise OSError(err_msg)

        self.consumer_key = os.getenv(_UsosApiConsumer.CONSUMER_KEY_VARNAME)
        self.consumer_secret = os.getenv(_UsosApiConsumer.CONSUMER_SECRET_VARNAME)


class UsosApi:
    """Class for interacting with USOS API

    It holds an instance of `UsosApiConsumer` and some functions
    that allow access to API both anonymously and with an user access token
    which is obtainable from `User` class instance

    All API interaction is wrapped with a decorator function `api_req()` that allows
    a request for failing several times (specified in `.env`) and retry connection
    """
    _consumer = None

    @classmethod
    def get_consumer(cls) -> _UsosApiConsumer:
        if UsosApi._consumer is None:
            UsosApi._consumer = _UsosApiConsumer()
        return UsosApi._consumer

    @classmethod
    @_api_req
    def anon_get(cls, url: str, *args, **kwargs):
        return requests.get(url, *args, **kwargs)

    @classmethod
    @_api_req
    def anon_post(cls, url: str, *args, **kwargs):
        return requests.post(url, *args, **kwargs)

    @classmethod
    @_api_req
    def user_get(cls, user: User, url: str, *args, **kwargs):
        return user.session.get(url, *args, **kwargs)

    @classmethod
    @_api_req
    def user_post(cls, user: User, url: str, *args, **kwargs):
        return user.session.post(url, *args, **kwargs)
