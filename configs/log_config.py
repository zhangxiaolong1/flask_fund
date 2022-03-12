# -*- coding: utf-8 -*-
# vela was here

import logging.config
from configs.config import current_config


def new_logger(logger_level, logger_name):
    logging.basicConfig(format='[%(asctime)s][%(levelname)s]%(message)s',
                        level=logger_level)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    log = logging.getLogger(logger_name)

    class NewLogger(object):
        def __init__(self, current_logger):
            self.logger = current_logger

        def debug(self, label=None, msg=None, data=None):
            self.logger.debug("[{}]{}:{}".format(label, msg, data))

        def info(self, label=None, msg=None, data=None):
            self.logger.info("[{}]{}:{}".format(label, msg, data))

        def warning(self, label=None, msg=None, data=None):
            self.logger.warning("[{}]{}:{}".format(label, msg, data))

        def critical(self, label=None, msg=None, data=None):
            self.logger.critical("[{}]{}:{}".format(label, msg, data))

    new_log = NewLogger(log)
    return new_log


logger = new_logger(current_config.log_level, "func_log")
