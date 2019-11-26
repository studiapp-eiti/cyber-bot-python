import mysql.connector
import os
from objects.user import User


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
        if USOSMySQLConnector.DB_NAME_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_USER_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_PASSWD_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_HOST_VARNAME not in os.environ.keys():
            raise OSError('Database-related environment variables not set')

        # TODO: Check for errors during connecting to the database
        self.connector = mysql.connector.connect(
            user=os.getenv(USOSMySQLConnector.DB_USER_VARNAME),
            password=os.getenv(USOSMySQLConnector.DB_PASSWD_VARNAME),
            host=os.getenv(USOSMySQLConnector.DB_HOST_VARNAME),
            database=os.getenv(USOSMySQLConnector.DB_NAME_VARNAME)
        )

    def get_usos_users(self) -> list:
        """Get all users' tokens, secrets and locale

        Returns a list of `User` objects
        """
        query = 'select {}, {}, {} from {};'.format(USOSMySQLConnector.COL_USOS_TOKEN,
                                                    USOSMySQLConnector.COL_USOS_TOKEN_SECRET,
                                                    USOSMySQLConnector.COL_USOS_LOCALE,
                                                    USOSMySQLConnector.TBL_USERS)
        users = []

        cursor = self.connector.cursor()
        cursor.execute(query)
        for (usos_token, usos_token_secret, locale) in cursor:
            users.append(User(usos_token, usos_token_secret, locale))
        cursor.close()

        return users

    def __del__(self):
        """Close connection with database"""
        if self.connector.is_connected():
            self.connector.close()
