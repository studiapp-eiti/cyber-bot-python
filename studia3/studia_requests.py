import requests
from bs4 import BeautifulSoup
import lxml
import json
import datetime
import time
import logging
import re

class Studia3Client:
    BASE_URL = "https://studia3.elka.pw.edu.pl/"
    SID_URL = "en/19Z/-/login/"
    LDAP_URL = "en/19Z/-/login-ldap"
    BASE_USER_URL = "https://studia3.elka.pw.edu.pl/en/19Z/-/ind/"
    URL_REFRESH_SESSION = "https://studia3.elka.pw.edu.pl/en/19Z/Time/login/"
    URL_BASE_FILE = "https://studia3.elka.pw.edu.pl/file"
    PARAM_URL_PUBLIC = "/pub"
    PARAM_URL_PROTECTED = "/lim"

    def __init__(self, sid_cookie, use_session=False, logger=None, term = "19Z"):
        """

        :type use_session: bool
        :type logger: logging.Logger
        """
        self.term = "/"+term
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

    def is_logged_in(self, times=1, delay=0):
        cookies = {"STUDIA_SID": self.cookie + "", "STUDIA_COOKIES": "YES"}
        status = None
        for _ in range(0, times):
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

    def get_contents(self, url):
        try:
            logged_in = self.log_in_for_scrapping()
        except TimeoutError:
            return False
        if logged_in:
            return self.session.get(url).text
        return False

    def determine_url_param(self, course):
        if self.log_in_for_scrapping():
            public_url = self.build_url(course, self.PARAM_URL_PUBLIC)
            protected_url = self.build_url(course, self.PARAM_URL_PROTECTED)




            public_contents = self.session.get(public_url).text
            protected_contents = self.session.get(protected_url).text
            reg = re.compile(r"(Access denied)")
            result = None
            if not reg.search(public_contents):
                result = "public"
            if not reg.search(protected_url):
                result = "protected"
            if result is None:
                return False # no access to public or protected pages



    def build_url(self, course_id, man_page_type, path=""):
        return self.URL_BASE_FILE + self.term + course_id + man_page_type + path
