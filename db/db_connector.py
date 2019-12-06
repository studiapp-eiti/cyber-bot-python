from os import getenv
import mysql.connector


class DbConnector:
    _CONNECTION = None
    DB_NAME_VARNAME = 'DB_NAME'
    DB_USER_VARNAME = 'DB_USER'
    DB_PASSWD_VARNAME = 'DB_PASSWD'
    DB_HOST_VARNAME = 'DB_HOST'

    @classmethod
    def get_connection(cls):
        """

        :rtype: mysql.connector.connection
        """
        if cls._CONNECTION is None:
            cls.log_in()
        return cls._CONNECTION

    @classmethod
    def log_in(cls):
        """Setup connection with database"""
        cls._CONNECTION = mysql.connector.connect(
            user=getenv(cls.DB_USER_VARNAME),
            password=getenv(cls.DB_PASSWD_VARNAME),
            host=getenv(cls.DB_HOST_VARNAME),
            database=getenv(cls.DB_NAME_VARNAME)
        )
