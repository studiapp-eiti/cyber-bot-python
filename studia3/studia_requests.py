import requests
from bs4 import BeautifulSoup
import lxml
import json
import datetime
import time
import logging


class Studia3Client:
    BASE_URL = "https://studia3.elka.pw.edu.pl/"
    SID_URL = "en/19Z/-/login/"
    LDAP_URL = "en/19Z/-/login-ldap"
    BASE_USER_URL = "https://studia3.elka.pw.edu.pl/en/19Z/-/ind/"
    URL_REFRESH_SESSION = "https://studia3.elka.pw.edu.pl/en/19Z/Time/login/"

    def __init__(self, sid_cookie, use_session=False, logger=None):
        """

        :type use_session: bool
        :type logger: logging.Logger
        """
        self.cookie = sid_cookie
        # self.expiration = exp_timestamp
        self.logger = logger
        self.cookies_dict = {"STUDIA_SID": sid_cookie + "", "STUDIA_COOKIES": "YES"}
        if use_session:
            self.session = requests.Session()

    def log_in_for_scrapping(self, timeout=5, times=2, delay=0):
        status = None
        response = None
        for _ in range(0, times):
            try:
                response = self.session.get(self.URL_REFRESH_SESSION, cookies=self.cookies_dict, timeout=timeout)
                status = True
                break
            except Exception:
                time.sleep(delay)
                self.logger.exception("Timeout occurred. Trying again")
        if status is None:
            raise TimeoutError(f"Could not get data from Studia3 Server. Timeout occurred {times} times.")
        return len(json.loads(response.text, encoding="UTF=8")["time"]) != 0  # If user is logged in, time parameter
        # will be present

    def get_contents(self, url):
        if self.log_in_for_scrapping():
            return self.session.get(url).text

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

    def is_logged_in(self, times=1, delay=0):
        cookies = {"STUDIA_SID": self.cookie + "", "STUDIA_COOKIES": "YES"}
        status = None
        for i in range(0, times):
            try:
                response = requests.get(self.URL_REFRESH_SESSION, cookies=cookies, timeout=5)
                status = True
                break
            except Exception:
                print("Request took too long")
                time.sleep(delay)
                status = None

        if status is True:
            parameters = json.loads(response.text, encoding="UTF-8")
            if len(parameters["time"]) == 0:
                return False
            return parameters["end"]
        return None
