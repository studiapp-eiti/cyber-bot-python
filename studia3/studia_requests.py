import requests
from bs4 import BeautifulSoup
import lxml
import json
import datetime
class Studia3Client:
    BASE_URL = "https://studia3.elka.pw.edu.pl/"
    SID_URL = "en/19Z/-/login/"
    LDAP_URL = "en/19Z/-/login-ldap"
    BASE_USER_URL = "https://studia3.elka.pw.edu.pl/en/19Z/-/ind/"
    URL_REFRESH_SESSION = "https://studia3.elka.pw.edu.pl/en/19Z/Time/login/"

    def __init__(self, sid_cookie):
        self.cookie = sid_cookie
        # self.expiration = exp_timestamp
        # self.session = requests.Session()

    # def get_sid(self):
    #     cookies = {"STUDIA_COOKIES": "YES"}
    #     url = ''.join([self.BASE_URL, self.SID_URL])
    #     response = self.session.get(url, cookies=cookies, headers={'Connection': 'keep-alive'})
    #     if response.status_code != 200:
    #         raise ValueError("Couldn't obtain cookie. The script will now terminate")
    #     return response.cookies.get_dict()["STUDIA_SID"]
    #
    # def log_in(self, username, password):
    #     payload = {"studia_uri": "", "studia_login": username, "studia_passwd": password, "zaloguj": "Zaloguj"}
    #     url = ''.join([self.BASE_URL, self.LDAP_URL])
    #     response = self.session.post(url, data=payload)
    #     if response.status_code == 200:
    #         self.cookie_sid = self.session.cookies.get_dict()["STUDIA_SID"]
    #         print(self.cookie_sid)
    #         return True
    #     raise ValueError("Please provide valid username and password!")

    def is_logged_in(self):
        cookies = {"STUDIA_SID": self.cookie+"", "STUDIA_COOKIES": "YES"}
        try:
            response = requests.get(self.URL_REFRESH_SESSION, cookies=cookies, timeout=5)
        except Exception:
            print("Request took too long")
            return None
        parameters = json.loads(response.text, encoding="UTF-8")
        if len(parameters["time"]) == 0:
            return None
        return parameters["end"]
