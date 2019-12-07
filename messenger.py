import requests
import json
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import ssl
from os import getenv

from usos.objects.points import Points

ssl.match_hostname = lambda cert, hostname: True
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Notifier:
    HEADERS = {"Accept": "*/*", "Cache-Control": "no-cache", "Content-Type": "application/json"}

    ENV_LOCAL_URL = "BOT_BASE_PATH"
    ENV_NOTIFY_URL = "BOT_NOTIFY_PATH"
    ENV_PUBLIC_URL = "BOT_BASE_PUBLIC_PATH"
    ENV_LOG_IN_URL = "BOT_STUDIA_LOGIN_PATH"

    def __init__(self, users):
        """

        :type users: list[int]
        """
        self.url = getenv(self.ENV_LOCAL_URL) + getenv(self.ENV_NOTIFY_URL)
        self.log_in_url = getenv(self.ENV_PUBLIC_URL)+getenv(self.ENV_LOG_IN_URL)
        self.users = users

    def call_api(self, other_params):
        payload = ({"user_ids": self.users})
        payload.update(other_params)
        response = requests.post(self.url, json=payload, headers=self.HEADERS, verify=False)
        return response.status_code == 200

    def message_session_expired(self):
        params = {"text": "Hey, $user.name Studia3 session has expired. Please log in again:", "message_type": "button",
                  "buttons":
                      [{"title": "Log in", "url": self.log_in_url}, ]}
        return self.call_api(params)

    def new_points(self, points: list):
        points_text = '\n'.join(['[{self.course_id}] {self.name}: {self.points} points'.format(self=p) for p in points])
        params = {"text": "Hey, $user.name you have new points!\n" + points_text, "message_type": "text"}
        return self.call_api(params)
