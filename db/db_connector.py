from os import getenv
import mysql.connector

from usos.log import UsosLogger


def db_operation(op):
    """Decorator function for automatically committing DB transactions or issuing a rollback if something goes wrong"""
    def dbop_wrapper(*args, **kwargs):
        ret = None
        try:
            ret = op(*args, **kwargs)
            DbConnector.get_connection().commit()
        except mysql.connector.Error:
            DbConnector.get_connection().rollback()
            # TODO: Raise RuntimeError and add logging
        return ret
    return dbop_wrapper


def db_operation_usos(op):
    """Same as `db_operation()` but specifically designed to USOS module for performing log operations during
    database operations"""
    def dbop_wrapper(*args, **kwargs):
        try:
            UsosLogger.db().debug('Trying to execute query...')
            ret = op(*args, **kwargs)
            DbConnector.get_connection().commit()
            UsosLogger.db().debug('Query executed successfully')
        except mysql.connector.Error as err:
            DbConnector.get_connection().rollback()
            err_msg = 'MySQL error occurred: {}'.format(err)
            UsosLogger.db().exception(err_msg)
            raise RuntimeError(err_msg)
        return ret
    return dbop_wrapper


class _DbConnection:
    """Class for connecting to MySQL DB"""

    # Environment variables names
    DB_NAME_VARNAME = 'DB_NAME'
    DB_USER_VARNAME = 'DB_USER'
    DB_PASSWD_VARNAME = 'DB_PASSWD'
    DB_HOST_VARNAME = 'DB_HOST'

    def __init__(self):
        """Connect to DB"""
        self.conn = mysql.connector.connect(
            user=getenv(_DbConnection.DB_USER_VARNAME),
            password=getenv(_DbConnection.DB_PASSWD_VARNAME),
            host=getenv(_DbConnection.DB_HOST_VARNAME),
            database=getenv(_DbConnection.DB_NAME_VARNAME),
            autocommit=False
        )

    def __del__(self):
        """Close connection with DB (if connected)"""
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()


class DbConnector:
    """Implements singleton behavior for `_DbConnection`"""
    _CONNECTION = None

    @classmethod
    def get_connection(cls) -> mysql.connector.connection.MySQLConnection:
        """ Return connection to the DB. Create one if it's called for the first time"""
        if cls._CONNECTION is None:
            cls._CONNECTION = _DbConnection()
        return cls._CONNECTION.conn
