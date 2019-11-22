import mysql.connector
import os
from usos.user import User


class USOSMySQLConnector:
    """Class used to connect to MySQL database and obtain USOS token"""

    # Environment variables names
    DB_NAME_VARNAME = 'DB_NAME'
    DB_USER_VARNAME = 'DB_USER'
    DB_PASSWD_VARNAME = 'DB_PASSWD'
    DB_HOST_VARNAME = 'DB_HOST'

    # Names related to `users` table
    TBL_USERS = 'users'
    COL_USOS_TOKEN = 'usos_token'
    COL_USOS_TOKEN_SECRET = 'usos_token_secret'
    COL_USOS_LOCALE = 'locale'

    def __init__(self):
        """Setup connection with MySQL database"""
        if self.DB_NAME_VARNAME not in os.environ.keys() \
                or self.DB_USER_VARNAME not in os.environ.keys() \
                or self.DB_PASSWD_VARNAME not in os.environ.keys() \
                or self.DB_HOST_VARNAME not in os.environ.keys():
            raise OSError('Database-related environment variables not set')

        # TODO: Check for errors during connecting to the database
        self._connector = mysql.connector.connect(
            user=os.getenv(self.DB_USER_VARNAME),
            password=os.getenv(self.DB_PASSWD_VARNAME),
            host=os.getenv(self.DB_HOST_VARNAME),
            database=os.getenv(self.DB_NAME_VARNAME)
        )

    def get_usos_users(self) -> list:
        """Get all users' tokens, secrets and locale

        Returns a list of `User` objects
        """
        query = 'select {}, {}, {} from {};'.format(self.COL_USOS_TOKEN,
                                                    self.COL_USOS_TOKEN_SECRET,
                                                    self.COL_USOS_LOCALE,
                                                    self.TBL_USERS)
        users = []

        cursor = self._connector.cursor()
        cursor.execute(query)
        for (usos_token, usos_token_secret, locale) in cursor:
            users.append(User(usos_token, usos_token_secret, locale))
        cursor.close()

        return users

    def close_connection(self):
        """Close connection with database"""
        if self._connector.is_connected():
            self._connector.close()
