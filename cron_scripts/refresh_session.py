import datetime
import sys

sys.path.insert(1, '/var/www/python')
from mysql_handler import db_handler

from studia3.studia_requests import Studia3Client

if __name__ == "__main__":
    database = db_handler.Db()
    maintainer_objects = database.get_cookies()
    for maintainer in maintainer_objects:
        exp_date = maintainer[2]
        id = maintainer[0]
        if (exp_date - datetime.datetime.now()).seconds <= 0:
            database.update_cookies(id)
        elif maintainer[1] is not None:  # 0 - maintainer Id, 1 - cookie, 2 - exp date
            client = Studia3Client(maintainer[1])
            new_exp_date = client.is_logged_in()
            database.update_cookies(id, new_exp_date)
