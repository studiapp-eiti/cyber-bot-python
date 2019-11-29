import mysql.connector
import mysql.connector.errors


class Queries:
    def __init__(self, db):
        """

        :type db: mysql.connector.MySQLConnection
        """
        self.db = db
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

    def update_cookies(self, m_id, expiration_date=None):
        if expiration_date is None:
            self.cursor.execute(f"UPDATE studia3_sessions SET cookie=NULL WHERE maintainer_id = {m_id}")
        else:
            self.cursor.execute(
                f"UPDATE studia3_sessions SET expires = FROM_UNIXTIME({expiration_date}) WHERE maintainer_id = {m_id} ")


