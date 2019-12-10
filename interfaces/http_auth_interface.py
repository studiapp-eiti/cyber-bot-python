import base64

from interfaces.base_interface import AuthenticationInterface


class HttpAuthInterface(AuthenticationInterface):

    def __init__(self, subject_id, options):
        self.username = options["username"]
        self.password = options["password"]

    def supported_subjects(self):
        return None

    def append_GET_parameters(self, existing_parameters=None):
        if existing_parameters is None:
            existing_parameters = dict()
        auth = (self.username + ":" + self.password)
        if "headers" not in existing_parameters:
            existing_parameters["headers"] = dict()
        existing_parameters["headers"]["Authorization"] = "Basic " + base64.b64encode(auth.encode("utf-8")).decode()
        return existing_parameters

    def subject_supported(self, s_id):
        return True
