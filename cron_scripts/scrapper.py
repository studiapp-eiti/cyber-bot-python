from db import db_connector
from studia3.studia3_mysql.queries import Queries
import pathlib
from dotenv import load_dotenv
from studia3.studia_requests import Studia3Client


def scrap():
    load_dotenv()
    db = db_connector.DBConnector()
    q = Queries(db)
    cookies = q.carry_transaction(lambda: q.get_cookies())
    if cookies:
        for cookie in cookies:
            print(Studia3Client.get_all_courses_urls(cookie["cookie"]))


if __name__ == "__main__":
    scrap()
