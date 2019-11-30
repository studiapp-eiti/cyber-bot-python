import requests
import json
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import ssl
from os import getenv
ssl.match_hostname = lambda cert, hostname: True
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class Notifier:
    HEADERS = {"Accept": "*/*", "Cache-Control": "no-cache", "Content-Type": "application/json"}
    ENV_BASE_URL = "BOT_BASE_PATH"
    ENV_NOTIFY_URL = "BOT_NOTIFY_PATH"

    def __init__(self, users):
        """

        :type users: list[int]
        """
        self.url = getenv(self.ENV_BASE_URL) + getenv(self.ENV_NOTIFY_URL)
        self.users = users

    def call_api(self, other_params):
        payload = ({"user_ids": self.users})
        payload.update(other_params)
        data = json.dumps(payload)
        response = requests.post(self.url, data=data, headers=self.HEADERS, verify=False)
        return response.status_code == 200

    def message_session_expired(self):
        params = {"text": "Hey, $user.name Studia3 session has expired. Please log in again:", "message_type": "button", "buttons":
            [{"title": "Log in", "url": "https://cyber-bot.westeurope.cloudapp.azure.com/n/studia3/login"}, ]}
        return self.call_api(params)

