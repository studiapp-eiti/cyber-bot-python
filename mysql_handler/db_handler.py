import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import os
import json
import datetime
from dotenv import load_dotenv
from pathlib import Path



class Db:
    def __init__(self):
        self.get_credentials()
        self.db = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
                                          passwd=os.getenv("DB_PASSWD"), database=os.getenv("DB_NAME"))
        self.cursor = self.db.cursor(dictionary=True)

    def get_cookies(self):
        self.cursor.execute('SELECT maintainer_id, cookie, expires FROM studia3_sessions')
        result = self.cursor.fetchall()
        return result

    def update_cookies(self, m_id, expiration_date=None):
        if expiration_date is None:
            self.cursor.execute(f"UPDATE studia3_sessions SET cookie=NULL WHERE maintainer_id = {m_id}")
        else:
            # mysql_dt =
            self.cursor.execute(f"UPDATE studia3_sessions SET expires = FROM_UNIXTIME({expiration_date}) WHERE maintainer_id = {m_id} ")
        self.db.commit()

    def __del__(self):
        self.cursor.close()
        self.db.close()


    @staticmethod
    def mysql_dt_format(timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def get_credentials():
        env_path = Path("..") / ".env"
        load_dotenv(dotenv_path=env_path)

