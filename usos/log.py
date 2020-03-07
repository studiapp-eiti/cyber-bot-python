import os
import logging
from pathlib import Path


class _UsosLog:
    """Class for log handling in USOS module

    It provides user with three main loggers:
    -> general logger
    -> database operation logger
    -> API operation logger

    Logging is performed to a file and to the stdout

    Log behaviour is somewhat configurable by setting proper
    environment variables - you can change log file path
    and file or stream logging level as well
    """

    # Environment variables names
    USOS_LOG_VARNAME = 'USOS_LOG_FILE'
    USOS_FILE_LEVEL_VARNAME = 'USOS_LOG_FILE_LEVEL'
    USOS_STREAM_LEVEL_VARNAME = 'USOS_LOG_STREAM_LEVEL'

    def __init__(self):
        """Set up main loggers"""
        if os.getenv(_UsosLog.USOS_LOG_VARNAME) is None \
                or os.getenv(_UsosLog.USOS_FILE_LEVEL_VARNAME) is None \
                or os.getenv(_UsosLog.USOS_STREAM_LEVEL_VARNAME) is None:
            raise OSError('Could not find env vars required by _UsosLog')

        self.gen_logger = logging.getLogger('usos')
        self.db_logger = self.gen_logger.getChild('db')
        self.api_logger = self.gen_logger.getChild('api')

        self.gen_logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        stream_formatter = logging.Formatter('[%(levelname)s] %(message)s')

        usos_log_path = Path(__file__).parents[1] / os.getenv(_UsosLog.USOS_LOG_VARNAME)

        file_handler = logging.FileHandler(usos_log_path)
        stream_handler = logging.StreamHandler()

        logging_levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        file_handler.setLevel(logging_levels[os.getenv(_UsosLog.USOS_FILE_LEVEL_VARNAME)])
        stream_handler.setLevel(logging_levels[os.getenv(_UsosLog.USOS_STREAM_LEVEL_VARNAME)])

        file_handler.setFormatter(file_formatter)
        stream_handler.setFormatter(stream_formatter)

        self.gen_logger.addHandler(file_handler)
        self.gen_logger.addHandler(stream_handler)


class UsosLogger:
    """Class for holding `_UsosLog` class instance in order to implement singleton behaviour

    It provides easy access to all three main loggers through class methods
    """
    _usos_log = None

    @classmethod
    def _get_instance(cls):
        if UsosLogger._usos_log is None:
            UsosLogger._usos_log = _UsosLog()
        return UsosLogger._usos_log

    @classmethod
    def gen(cls):
        return UsosLogger._get_instance().gen_logger

    @classmethod
    def db(cls):
        return UsosLogger._get_instance().db_logger

    @classmethod
    def api(cls):
        return UsosLogger._get_instance().api_logger
