import logging
import datetime

from modules import common


class LogMessages:
    @staticmethod
    def send_detailed_info(from_module: str, from_function: str, message: str):
        log_message = f'Module: {from_module} \nFunction name: {from_function} \nMessage: {message}'
        logging.info(log_message)

    @staticmethod
    def send_tracking_info(from_module: str, message: str):
        log_message = f'Module: {from_module} \nMessage: {message}'
        logging.info(log_message)

    @staticmethod
    def send_info(message: str):
        log_message = message
        logging.info(log_message)

    @staticmethod
    def send_warning_info(message: str | Exception):
        logging.warning(message)

    @staticmethod
    def throw_error(error: str | Exception):
        logging.error(error)

    @staticmethod
    def throw_critical_error(error: str | Exception):
        logging.critical(error)


def get_datetime_now_str() -> str:
    datetime_now = datetime.datetime.now()
    datetime_now_str = datetime_now.strftime('%d.%m.%Y %H-%M')
    return datetime_now_str


def get_log_filename(name: str):
    filename = name + '.log'
    return filename


def create_logfile(postfix: str):
    datetime_str = get_datetime_now_str()

    log_name = datetime_str + ' ' + postfix
    log_filename = get_log_filename(log_name)
    log_path = common.get_log_path().joinpath(log_filename)

    open(log_path, mode='a').close()
    return log_path


class Logger:
    cmd_handler: logging.StreamHandler
    session_handler: logging.FileHandler
    error_handler: logging.FileHandler

    def __init__(self):
        log_format = '%(asctime)s %(levelname)s %(message)s'
        asctime_format = '%H:%M:%S'

        self.cmd_handler = logging.StreamHandler()
        self.session_handler = self.create_session_handler()
        self.error_handler = self.create_error_handler()

        logging.basicConfig(level=logging.DEBUG,
                            format=log_format,
                            datefmt=asctime_format,
                            handlers=(self.cmd_handler, self.session_handler, self.error_handler))

    @staticmethod
    def create_session_handler():
        session_path = create_logfile('session')
        session_handler = logging.FileHandler(session_path)
        session_handler.setLevel(logging.INFO)
        return session_handler

    @staticmethod
    def create_error_handler():
        error_path = create_logfile('error')
        error_handler = logging.FileHandler(error_path)
        error_handler.setLevel(logging.ERROR)
        return error_handler
