import mysql.connector
import os


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

    def __init__(self):
        """Setup connection with MySQL database"""
        if USOSMySQLConnector.DB_NAME_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_USER_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_PASSWD_VARNAME not in os.environ.keys() \
                or USOSMySQLConnector.DB_HOST_VARNAME not in os.environ.keys():
            raise OSError('Database-related environment variables not set')

        # TODO: Check for errors during connecting to the database
        self._connector = mysql.connector.connect(
            user=os.getenv(USOSMySQLConnector.DB_USER_VARNAME),
            password=os.getenv(USOSMySQLConnector.DB_PASSWD_VARNAME),
            host=os.getenv(USOSMySQLConnector.DB_HOST_VARNAME),
            database=os.getenv(USOSMySQLConnector.DB_NAME_VARNAME)
        )

    def get_usos_tokens(self) -> list:
        """Get all users' tokens from databse

        Tokens are returned in a list containing dictionaries in following format:
        {'token': usertoken, 'secret': usersecret}
        """
        query = 'select {}, {} from {};'.format(USOSMySQLConnector.COL_USOS_TOKEN,
                                                USOSMySQLConnector.COL_USOS_TOKEN_SECRET,
                                                USOSMySQLConnector.TBL_USERS)
        usos_tokens = []

        cursor = self._connector.cursor()
        # TODO: Check for errors during executing the query
        cursor.execute(query)
        for (usos_token, usos_token_secret) in cursor:
            usos_tokens.append({'token': usos_token, 'secret': usos_token_secret})
        cursor.close()

        return usos_tokens

    def close_connection(self):
        """Close connection with database"""
        if self._connector.is_connected():
            self._connector.close()
