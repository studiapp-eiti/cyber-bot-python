import requests
import json
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Notifier:
    HEADERS = {"Accept": "*/*", "Cache-Control": "no-cache", "Content-Type": "application/json"}
    URL = "https://localhost:8083/messenger/notify"

    def __init__(self, users):
        """

        :type users: list
        """
        self.users = users

    def call_api(self, other_params):
        payload = ({"user_ids": self.users})
        payload.update(other_params)
        data = json.dumps(payload)
        print(data)
        response = requests.post(self.URL, data=data, headers=self.HEADERS, verify=False)
        print(response.content)
        return response.status_code == 200

    def message_session_expired(self):
        params = {"text": "Hey, $user.name Studia3 session has expired. Please log in again:", "message_type": "button", "buttons":
            [{"title": "Log in", "url": "https://cyber-bot.westeurope.cloudapp.azure.com/n/studia3/login"}, ]}
        return self.call_api(params)
