from os import getenv
import mysql.connector


class DBConnector:
    """Class for handling connection with MySQL database"""

    # Environment variables names
    DB_NAME_VARNAME = 'DB_NAME'
    DB_USER_VARNAME = 'DB_USER'
    DB_PASSWD_VARNAME = 'DB_PASSWD'
    DB_HOST_VARNAME = 'DB_HOST'

    def __init__(self):
        """Setup connection with database"""
        self.connection = mysql.connector.connect(
            user=getenv(DBConnector.DB_USER_VARNAME),
            password=getenv(DBConnector.DB_PASSWD_VARNAME),
            host=getenv(DBConnector.DB_HOST_VARNAME),
            database=getenv(DBConnector.DB_NAME_VARNAME)
        )

    def __del__(self):
        """Close connection if connected"""
        if self.connection.is_connected():
            self.connection.close()
