import logging
import sys

from time import localtime, strftime


class StandardLogger(object):
    def __init__(self, module_name, level_name="INFO"):
        self.module_name = module_name

        if isinstance(level_name, int):
            self.log_level = level_name
        else:
            self.log_level = logging.getLevelName(level_name)

    def format_message(self, level_name, msg, error=None):
        try:
            if not error:
                return "{} ({}) {} - {}\n".format(strftime("%Y-%m-%d %H:%M:%S", localtime()), level_name, self.module_name, msg)

            return "{} ({}) {} - {} : Error={}\n".format(strftime("%Y-%m-%d %H:%M:%S", localtime()), level_name, self.module_name, msg, error.message)
        except:
            return "{} ({}) {} - {}\n".format(strftime("%Y-%m-%d %H:%M:%S", localtime()), level_name, self.module_name, msg)

    def setLevel(self, level):
        self.log_level = level

    def debug(self, msg):
        if self.log_level <= logging.getLevelName("DEBUG"):
            sys.stdout.write(self.format_message("DEBUG", msg))

    def info(self, msg):
        if self.log_level <= logging.getLevelName("INFO"):
            sys.stdout.write(self.format_message("INFO", msg))

    def warn(self, msg, error=None):
        self.warning(msg, error)

    def warning(self, msg, error=None):
        if self.log_level <= logging.getLevelName("WARNING"):
            sys.stdout.write(self.format_message("WARNING", msg, error))

    def error(self, msg, error=None):
        if self.log_level <= logging.getLevelName("ERROR"):
            sys.stderr.write(self.format_message("ERROR", msg, error))

    def critical(self, msg, error=None):
        if self.log_level <= logging.getLevelName("CRITICAL"):
            sys.stderr.write(self.format_message("CRITICAL", msg, error))

    def isEnabledFor(self, log_level):
        return self.log_level <= log_level
