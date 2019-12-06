from .base_interface import AuthenticationInterface
from studia3.studia3_mysql.queries import Queries
import requests


class Studia3Interface(AuthenticationInterface):
    COOKIES = {"STUDIA_SID": "", "STUDIA_COOKIES": "YES"}

    def __init__(self, subject_id, *args, **kwargs):
        self.subjects = self.supported_subjects()
        self.cookie_session_id = self.subject_supported(subject_id)

    def supported_subjects(self):
        query = Queries.get_instance()
        result = query.carry_transaction(query.get_accessible_subject)
        supported_subjects = dict()
        for line in result:
            supported_subjects[line["cookie"]] = line["usos_courses"].split(";")
        return supported_subjects

    def subject_supported(self, s_id):
        result = next((k for k, v in self.subjects.items() if s_id in v), False)
        if result is False:
            raise ValueError(f"This subject ({s_id}) is not supported by the {self.__name__}")
        return result

    def get_request_parameters(self, r_parameters=None):
        if r_parameters is None:
            r_parameters = dict()

        cookies = self.COOKIES.copy()
        cookies["STUDIA_SID"] = self.cookie_session_id
        r_parameters["cookies"] = cookies
        return r_parameters

