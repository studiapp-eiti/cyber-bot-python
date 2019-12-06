import mysql.connector
import mysql.connector.errors
from db import db_connector


class Queries:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls._INSTANCE is None:
            cls._INSTANCE = Queries()
        return cls._INSTANCE

    def __init__(self):
        """

        :type db: db.DbConnector
        """

        self.db = db_connector.DbConnector.get_connection()
        self.cursor = None

    def carry_transaction(self, fun, commitable=False):
        self.cursor = self.db.cursor(dictionary=True)
        try:
            to_ret = fun()
        except mysql.connector.errors.DatabaseError:
            self.db.rollback()
            commitable = False
            to_ret = False

        if commitable:
            self.db.commit()

        self.cursor.close()
        self.cursor = None
        return to_ret

    def get_cookies(self):
        self.cursor.execute('SELECT maintainer_id, cookie, expires FROM studia3_sessions')
        result = self.cursor.fetchall()
        return result

    def get_accessible_subject(self):
        query = "SELECT studia3_sessions.maintainer_id, studia3_sessions.cookie, u.usos_courses " \
                "FROM studia3_sessions LEFT JOIN users u on studia3_sessions.maintainer_id = u.id"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_cookies(self, m_id, expiration_date=None):
        if expiration_date is None:
            self.cursor.execute(f"UPDATE studia3_sessions SET cookie=NULL WHERE maintainer_id = {m_id}")
        else:
            self.cursor.execute(
                f"UPDATE studia3_sessions SET expires = FROM_UNIXTIME({expiration_date}) WHERE maintainer_id = {m_id} ")
