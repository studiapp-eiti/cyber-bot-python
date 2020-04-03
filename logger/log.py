import os
import logging
from pathlib import Path


class _Log:
    """Class for log handling

    There is one general logger ('gen') and for USOS and studia3 modules
    there are two separate ones

    For USOS module it provides user with three main loggers:
    -> general module logger ('usos')
    -> database operation logger ('usos.db')
    -> API operation logger ('usos.api')

    For studia3 module there are two loggers for now:
    -> general module logger ('studia')
    -> database operation logger ('studia.db')

    Logging is performed to a file and to the stdout

    You can adjust logging levels both for file and stream handlers
    by setting proper environment variables
    """

    # Environment variables names
    FILE_LEVEL_VARNAME = 'LOG_FILE_LEVEL'
    STREAM_LEVEL_VARNAME = 'LOG_STREAM_LEVEL'
    LOG_PATH_VARNAME = 'BOT_LOG_PATH'

    def __init__(self):
        """Set up main loggers

        If `BOT_LOG_PATH` environment variable is not set
        it attempts to find log path up to 2 directories above
        where the `__file__` points to. The log path is just
        a directory named 'log'
        """
        if os.getenv(_Log.FILE_LEVEL_VARNAME) is None \
                or os.getenv(_Log.STREAM_LEVEL_VARNAME) is None:
            raise OSError('Could not find env vars required by _Log')

        self.gen_logger = logging.getLogger('gen')

        self.usos_logger = logging.getLogger('usos')
        self.usos_db_logger = self.usos_logger.getChild('db')
        self.usos_api_logger = self.usos_logger.getChild('api')

        self.studia3_logger = logging.getLogger('studia')
        self.studia3_db_logger = self.studia3_logger.getChild('db')

        self.gen_logger.setLevel(logging.DEBUG)
        self.usos_logger.setLevel(logging.DEBUG)
        self.studia3_logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        stream_formatter = logging.Formatter('[%(levelname)s] %(message)s')

        # Find log directory
        log_path = None

        if os.getenv(_Log.LOG_PATH_VARNAME) is not None:
            log_path = os.getenv(_Log.LOG_PATH_VARNAME)
        else:
            for i in range(3):  # Seek up to 2 directories above
                for file in Path(__file__).parents[i].iterdir():
                    if file.is_dir() and file.name == 'log':
                        log_path = file.absolute()

        if log_path is None:
            raise OSError('Could not find log destination directory')

        usos_log_path = Path(log_path) / 'usos.log'
        studia3_log_path = Path(log_path) / 'studia.log'

        usos_file_handler = logging.FileHandler(usos_log_path)
        studia3_file_handler = logging.FileHandler(studia3_log_path)
        stream_handler = logging.StreamHandler()

        logging_levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        usos_file_handler.setLevel(logging_levels[os.getenv(_Log.FILE_LEVEL_VARNAME)])
        studia3_file_handler.setLevel(logging_levels[os.getenv(_Log.FILE_LEVEL_VARNAME)])
        stream_handler.setLevel(logging_levels[os.getenv(_Log.STREAM_LEVEL_VARNAME)])

        usos_file_handler.setFormatter(file_formatter)
        studia3_file_handler.setFormatter(file_formatter)
        stream_handler.setFormatter(stream_formatter)

        self.gen_logger.addHandler(usos_file_handler)
        self.gen_logger.addHandler(studia3_file_handler)
        self.gen_logger.addHandler(stream_handler)

        self.usos_logger.addHandler(usos_file_handler)
        self.usos_logger.addHandler(stream_handler)

        self.studia3_logger.addHandler(studia3_file_handler)
        self.studia3_logger.addHandler(stream_handler)


class Log:
    """Singleton behaviour for _Log class"""
    _logger = None

    @classmethod
    def _get_instance(cls):
        if Log._logger is None:
            Log._logger = _Log()
        return Log._logger

    @classmethod
    def gen(cls):
        return Log._get_instance().gen_logger

    @classmethod
    def usos(cls):
        return Log._get_instance().usos_logger

    @classmethod
    def u_db(cls):
        return Log._get_instance().usos_db_logger

    @classmethod
    def u_api(cls):
        return Log._get_instance().usos_api_logger

    @classmethod
    def studia(cls):
        return Log._get_instance().studia3_logger

    @classmethod
    def s_db(cls):
        return Log._get_instance().studia3_db_logger
