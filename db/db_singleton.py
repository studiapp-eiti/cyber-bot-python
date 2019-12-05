from os import getenv
from .db_connector import DBConnector
import mysql.connector

class DbConnectorS:
    _CONNECTION = None
    DB_NAME_VARNAME = 'DB_NAME'
    DB_USER_VARNAME = 'DB_USER'
    DB_PASSWD_VARNAME = 'DB_PASSWD'
    DB_HOST_VARNAME = 'DB_HOST'

    @classmethod
    def get_connection(cls):
        if cls._CONNECTION is None:
            cls.log_in()
        return cls._CONNECTION

    @classmethod
    def log_in(cls):
        """Setup connection with database"""
        cls._CONNECTION = mysql.connector.connect(
            user=getenv(DBConnector.DB_USER_VARNAME),
            password=getenv(DBConnector.DB_PASSWD_VARNAME),
            host=getenv(DBConnector.DB_HOST_VARNAME),
            database=getenv(DBConnector.DB_NAME_VARNAME)
        )
