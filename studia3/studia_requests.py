import requests


class Studia3Client:
    BASE_URL = "https://studia3.elka.pw.edu.pl/"
    SID_URL = "en/19Z/-/login/"
    LDAP_URL = "en/19Z/-/login-ldap"
    COOKIE_SID = None

    def __init__(self):
        self.session = requests.Session()
        self.cookie_sid = self.get_sid()

    def get_sid(self):
        cookies = {"STUDIA_COOKIES": "YES"}
        url = ''.join([self.BASE_URL, self.SID_URL])
        response = self.session.get(url, cookies=cookies, headers={'Connection': 'keep-alive'})
        if response.status_code != 200:
            raise ValueError("Couldn't obtain cookie. The script will now terminate")
        return response.cookies.get_dict()["STUDIA_SID"]

    def log_in(self, username, password):
        payload = {"studia_uri": "", "studia_login": username, "studia_passwd": password, "zaloguj": "Zaloguj"}
        url = ''.join([self.BASE_URL, self.LDAP_URL])
        response = self.session.post(url, data=payload)
        if response.status_code == 200:
            self.cookie_sid = self.session.cookies.get_dict()["STUDIA_SID"]
            return True

        raise ValueError("Please provide valid username and password!")

