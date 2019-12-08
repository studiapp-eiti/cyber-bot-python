from .base_interface import AuthenticationInterface
from studia3.studia3_mysql.queries import Queries
import requests


class Studia3Interface(AuthenticationInterface):
    COOKIES = {"STUDIA_SID": "", "STUDIA_COOKIES": "YES"}

    def __init__(self, subject_id, *args, **kwargs):
        self.supported_subjects = self.supported_subjects()
        self.cookie_session_id = self.subject_supported(subject_id)

    def supported_subjects(self):
        query = Queries.get_instance()
        result = query.carry_transaction(query.get_accessible_subject)
        supported_subjects = dict()
        for line in result:
            supported_subjects[line["cookie"]] = [int(x) for x in line["usos_courses"].split(";")]
        return supported_subjects

    def subject_supported(self, s_id):
        result = next((k for k, v in self.supported_subjects.items() if s_id in v), False)
        if result is False:
            raise ValueError(f"This subject ({s_id}) is not supported by the {__name__}")
        return result

    def append_GET_parameters(self, existing_parameters: dict = None) -> dict:
        if existing_parameters is None:
            existing_parameters = dict()

        cookies = self.COOKIES.copy()
        cookies["STUDIA_SID"] = self.cookie_session_id
        existing_parameters["cookies"] = cookies

        return dict(params=existing_parameters)
