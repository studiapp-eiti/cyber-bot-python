import datetime
import sys
import os
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mysql_handler import db_handler
from studia3.studia_requests import Studia3Client
import messenger

if __name__ == "__main__":
    database = db_handler.Db()
    maintainers = database.get_cookies()
    to_be_notified = list()
    for maintainer in maintainers:
        if maintainer["cookie"] is not None:
            delta = maintainer["expires"].timestamp() - datetime.datetime.now().timestamp()
            m_id = maintainer["maintainer_id"]
            if delta <= 0:
                database.update_cookies(m_id)
                to_be_notified.append(m_id)
            else:
                client = Studia3Client(maintainer["cookie"])
                new_exp_date = client.is_logged_in()
                database.update_cookies(m_id, new_exp_date)
                if new_exp_date is not None:
                    time.sleep(random.randrange(5, 30))
                else:
                    to_be_notified.append(m_id)
    if len(to_be_notified) is not 0:
        N = messenger.Notifier(to_be_notified)
        N.message_session_expired()
