from os import getenv
import mysql.connector

from logger.log import Log


def db_safe_transaction(log_name: str):
    """Decorator function for performing safe MySQL database transactions which will be auto-committed
    is case of successful operation or rollback will be issued if something goes wrong

    There is also support for logging: you simply specify which module do you use (USOS or studia3)
    and information about DB operations will be logged to corresponding loggers

    :param log_name: Log name. Only 'usos' and 'studia' are supported for now
    """
    def db_transaction(operation):
        def db_transaction_wrapper(*args, **kwargs):
            assert log_name in ['usos', 'studia'], 'Only \'usos\' and \'studia\' log names are allowed'

            logger = None
            if log_name == 'usos':
                logger = Log.u_db()
            elif log_name == 'studia':
                logger = Log.s_db()

            try:
                logger.debug('Trying to execute query...')
                ret = operation(*args, **kwargs)
                DbConnector.get_connection().commit()
                logger.debug('Query executed successfully')
            except mysql.connector.Error as err:
                DbConnector.get_connection().rollback()
                err_msg = 'MySQL error occurred: {}'.format(err)
                logger.exception(err_msg)
                raise RuntimeError(err_msg)
            return ret
        return db_transaction_wrapper
    return db_transaction


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
