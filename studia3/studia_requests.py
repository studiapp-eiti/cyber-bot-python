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
    BASE_USER_URL = "https://studia3.elka.pw.edu.pl/en/19Z/"
    URL_REFRESH_SESSION = "https://studia3.elka.pw.edu.pl/en/19Z/Time/login/"
    URL_BASE_FILE = "https://studia3.elka.pw.edu.pl/file"
    PARAM_URL_PUBLIC = "/pub"
    PARAM_URL_PROTECTED = "/lim"

    COOKIES = {"STUDIA_SID": "", "STUDIA_COOKIES": "YES"}

    def __init__(self, sid_cookie, use_session=False, logger=None, term="19Z"):
        """

        :type use_session: bool
        :type logger: logging.Logger
        """
        self.term = "/" + term
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

    @classmethod
    def is_logged_in(cls, session_id_cookie):
        response = cls.get_contents(session_id_cookie, cls.URL_REFRESH_SESSION)
        data = json.loads(response.text, encoding="UTF-8")
        if data is None:
            return None
        if len(data["time"]) == 0:
            return False
        return data["end"]

    @staticmethod
    def get_contents(session_id: str, url: str, timeout=5):
        """
        :type: session_id: str

        :rtype: requests.response
        """
        cookies = Studia3Client.COOKIES.copy()
        cookies["STUDIA_SID"] = session_id
        try:
            response = requests.get(url, cookies=cookies, timeout=timeout)
        except Exception:
            print("Request took too long")
            return None
        return response

    @classmethod
    def get_contents_with_check(cls, session_id, url, timeout=5):
        if cls.is_logged_in(session_id):
            return cls.get_contents(session_id, url, timeout)
        return False

    @classmethod
    def get_all_courses_urls(cls, session_id):
        response = cls.get_contents_with_check(session_id, cls.BASE_USER_URL)
        if response:
            ret = dict()
            matches = list(re.finditer(
                r'<a.*?href=["\'](?P<url>/file/\d{2}[ZL]/(?P<id>[A-Za-z-\d].+?)/\w.+?/)["\'].+?</a>', response.text))
            if len(matches) == 0:
                return None
            for match in matches:
                match = match.groupdict()
                ret[match["id"]] = match["url"]
            return ret
        return False

    def build_url(self, course_id, man_page_type, path=""):
        return self.URL_BASE_FILE + self.term + course_id + man_page_type + path
