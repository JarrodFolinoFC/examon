import logging
from logging.handlers import RotatingFileHandler


def decorator_timer(some_function):
    def wrapper(*args, **kwargs):
        from time import time
        t1 = time()
        result = some_function(*args, **kwargs)
        end = time() - t1
        LoggerFactory.instance().info(f'{some_function.__name__} time: {end}')
        return result, end

    return wrapper


handlers = [RotatingFileHandler(filename='/tmp/examon.log',
                                mode='w',
                                maxBytes=512000,
                                backupCount=4)
            ]
logging.basicConfig(handlers=handlers,
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y%I:%M:%S %p')


class LoggerFactory:
    log_file_name = '/tmp/examon.log'

    @staticmethod
    def instance():
        return logging.getLogger('my_logger')
