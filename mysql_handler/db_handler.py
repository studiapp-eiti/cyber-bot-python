import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import os
import json
import datetime


class Db:
    def __init__(self):
        credentials = self.get_credentials()
        self.db = mysql.connector.connect(host="localhost", user=credentials["username"],
                                          passwd=credentials["password"], database=credentials["db"])
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

    @classmethod
    def get_credentials(cls):
        full_path = os.path.realpath(__file__)
        path, _ = os.path.split(full_path)
        credentials = None
        with open(path + "/../.env/credentials.json") as f:
            credentials = json.load(f)
        return credentials["mysql"]
