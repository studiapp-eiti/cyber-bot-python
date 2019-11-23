import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mysql_handler import db_handler
from studia3 import studia_requests




def scrap():
    # Fetch Ids and courses from DB TODO do it properly for users from users table, not from studia_sessions
    db = db_handler.Db()
    maintainers = db.get_cookies()
    for user in maintainers:
        cookie = user["cookie"]
        studia3_client = studia_requests.Studia3Client(cookie, use_session=True)
