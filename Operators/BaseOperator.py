import ConfigParser
import logging
import os
import random
import string
import sys
import datetime
import subprocess
import shlex
from abc import ABCMeta, abstractmethod

logging.basicConfig(level=logging.INFO)


class NoConfigException(BaseException):

    def __init__(self, victim, filepath):
        victim.logger.fatal("No fuch file as config file {}".format(filepath))
        super(NoConfigException, self).__init__()
        sys.exit(1)

class NoAccessConfigException(BaseException):

    def __init__(self, filepath):
        logging.fatal("Can't read config file {}".format(filepath))
        super(NoAccessConfigException, self).__init__()
        sys.exit(2)


def randomname(n):
    return "".join([random.choice(string.hexdigits) for X in range(n)])


class BaseOperator(object):
    __metaclass__ = ABCMeta
    configpath = ""
    moment = datetime.datetime.now()

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stagepath = os.path.join("/tmp", randomname(16))
        self.logger.info("Creation with stage path {}".format(self.stagepath))

    @classmethod
    def setconfigpath(self, path):
        self.configpath = path

    def _loadconfig(self, confpath):
        if not os.path.exists(confpath):
            raise NoConfigException(self, confpath)
        if not os.access(confpath, 4):
            raise NoAccessConfigException(confpath)
        out = ConfigParser.ConfigParser()
        out.read(confpath)
        self.config = out

    def setpredecesor(self, predecesor):
        self.predecesor = predecesor
        self.logger.info("Input data will be taken from {}".format(self.predecesor.stagepath))

    def verify(self):
        pass

    # @abstractmethod
    def run(self):
        pass

    def _run_wrapped(self, command):
        with open("", "w") as fwout, open("", "w") as fwerr:
            process = subprocess.Popen(shlex.split(command), stdout=fwout, stderr=fwerr)
            print process.returncode

