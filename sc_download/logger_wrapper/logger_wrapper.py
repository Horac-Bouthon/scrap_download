import logging
import logging.handlers
import logger_wrapper
import os


class LoggerWrapper:

    @staticmethod
    def set_logger(logger, verbose=False, log_level=None):
        return_val = logger
        if log_level is not None:
            str_level = log_level
        else:
            str_level = logger_wrapper.LOG_LEVEL
        level = logging.ERROR
        if 'WARNING' in str_level:
            level = logging.WARNING
        if 'INFO' in str_level:
            level = logging.INFO
        if 'DEBUG' in str_level:
            level = logging.DEBUG
        return_val.setLevel(level)
        folder = logger_wrapper.LOG_FILE
        # check end create folder
        dir_tc = os.path.dirname(os.path.abspath(folder))
        if not os.path.isdir(dir_tc):
            os.mkdir(dir_tc)
        max_bytes = logger_wrapper.MAX_BYTES
        if max_bytes < 1024:
            max_bytes = 1024
        max_count = logger_wrapper.MAX_COUNT
        if max_count < 1 or max_count > 10:
            max_count = 10
        fh = logging.handlers.RotatingFileHandler(folder, maxBytes=max_bytes, backupCount=max_count)
        fh.setLevel(level)
        ch = logging.StreamHandler()
        if verbose:
            ch.setLevel(logging.INFO)
        else:
            ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        return_val.addHandler(ch)
        return_val.addHandler(fh)
        return return_val

    def __init__(self):
        pass

    def __repr__(self):
        return "LoggerWrapper()"

    def __str__(self):
        return 'LoggerWrapper'
