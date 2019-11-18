import datetime
import sys
import os
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mysql_handler import db_handler
from studia3.studia_requests import Studia3Client

if __name__ == "__main__":
    database = db_handler.Db()
    maintainers = database.get_cookies()
    for maintainer in maintainers:
        exp_date = maintainer[2]
        id = maintainer[0]
        delta = exp_date.timestamp() - datetime.datetime.now().timestamp()
        if delta <= 0:
            database.update_cookies(id)
        elif maintainer[1] is not None:  # 0 - maintainer Id, 1 - cookie, 2 - exp date
            client = Studia3Client(maintainer[1])
            new_exp_date = client.is_logged_in()
            database.update_cookies(id, new_exp_date)
            if new_exp_date is not None:
                time.sleep(random.randrange(5, 30))
