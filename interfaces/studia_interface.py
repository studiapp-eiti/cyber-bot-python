from .base_interface import HttpInterface
import requests


class Studia3Interface(HttpInterface):
    COOKIES = {"STUDIA_SID": "", "STUDIA_COOKIES": "YES"}
    URL_REFRESH_SESSION = "https://studia3.elka.pw.edu.pl/en/19Z/Time/login/"

    def __init__(self, subject_id, *args, **kwargs):
        self.subject_id = subject_id
        self.db = queries
        self.subjects = self.supported_subjects()
        result = self.subject_supported(subject_id)
        if not result:
            raise ValueError(f"This subject ({subject_id}) is not supported by the {self.__name__}")
        self.cookie_session_id = result

    def supported_subjects(self):
        result = self.db.carry_transaction(self.db.get_accessible_subject)
        supported_subjects = dict()
        for line in result:
            supported_subjects[line["cookie"]] = line["usos_courses"].split(";")
        return supported_subjects

    def subject_supported(self, s_id):
        return next((k for k, v in self.subjects.items() if s_id in v), False)

    def is_logged_in(self):
        response = self.get_contents(self.URL_REFRESH_SESSION)
        data = response.json()
        if data is None:
            return False
        return len(data["time"]) != 0

    def get_contents(self, url, timeout=5):
        """
        :type: session_id: str
        :rtype: requests.get()
        """
        cookies = self.COOKIES.copy()
        cookies["STUDIA_SID"] = self.cookie_session_id
        try:
            response = requests.get(url, cookies=cookies, timeout=timeout)
        except Exception:
            print("Request took too long")
            return None
        return response

    def get_scrapping_data(self, url, timeout=5):
        if self.is_logged_in():
            return self.get_contents(url, timeout).text
        raise ConnectionError(f"User is not logged in to scrap this subject: {self.subject_id}")
