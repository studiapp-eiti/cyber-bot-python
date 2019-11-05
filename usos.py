import rauth
import os


class USOS_Connection:
    def __init__(self):
        base_url = 'https://apps.usos.pw.edu.pl/'
        req_token_url = 'services/oauth/request_token'
        auth_url = 'services/oauth/authorize'
        acc_token_url = 'services/oauth/access_token'

        consumer_key, consumer_secret = self._obtain_api_key()  # File with credentials should be in the same path

        self._service = rauth.OAuth1Service(consumer_key=consumer_key,
                                           consumer_secret=consumer_secret,
			                   name='USOSAPI',
			                   request_token_url=req_token_url,
			                   authorize_url=auth_url,
			                   access_token_url=acc_token_url,
			                   base_url=base_url)


        request_token, request_token_secret = self._service.get_request_token(params={
            'oauth_callback': 'oob',  # We don't specify callback URL (yet)
            'scopes':'grades|studies'  # What information we want to have access to
        })

        print('Go to this URL to authorize: ', base_url + self._service.get_authorize_url(request_token))
        pin = input('Enter PIN: ')

        self._session = self._service.get_auth_session(request_token,
                                                     request_token_secret,
                                                     method='POST',
                                                     data={'oauth_verifier': pin})


    def _obtain_api_key(self) -> tuple:
        client_id_var = 'USOS_API_CLIENT_ID'
        client_secret_var = 'USOS_API_CLIENT_SECRET'

        if client_id_var not in os.environ.keys() or client_secret_var not in os.environ.keys():
            raise OSError('USOS API Client credentials not set in system environment')
            
        return os.environ[client_id_var], os.environ[client_secret_var]


    def get_class_schedule(self, days: int):
        assert (days <= 7 and days > 0), 'You can include no more than 7 days in schedule'
        print(self._session.get('services/tt/student', params={'days': days}).text)


    def get_recent_grades(self):
        print(self._session.get('services/grades/latest').text)
