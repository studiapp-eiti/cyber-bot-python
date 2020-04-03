import requests
from urllib3.exceptions import InsecureRequestWarning
import ssl
from os import getenv

from usos.obj.points import Points
from usos.obj.timetable import Timetable

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
        self.log_in_url = getenv(self.ENV_PUBLIC_URL) + getenv(self.ENV_LOG_IN_URL)
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

    def message_updated_points(self, points, new_points: bool) -> bool:
        """Send notification about new points on USOS

        :param points: List of new points
        :type points: list[Points]
        :param new_points: Are points new (that means: no updated)
        :returns: `True` when notification was successfully sent, `False` otherwise
        """
        if len(points) != 0:
            points_text = 'Hey $user.name, you have '
            if new_points:
                points_text += 'new'
            else:
                points_text += 'updated'
            points_text += ' points.'
            course_ids = {p.course_id for p in points}
            for course_id in sorted(course_ids):
                related_points = sorted([p for p in points if p.course_id == course_id], key=lambda x: x.name)
                points_text += '\n\n[{}]\n{}'.format(
                    course_id.split('-')[-1],
                    '\n'.join(['{}: {}'.format(rp.name, rp.points) for rp in related_points])
                )

            params = {"text": points_text}
            return self.call_api(params)
        else:
            return False
