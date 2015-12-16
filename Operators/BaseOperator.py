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
import hashlib
import fcntl

logging.basicConfig(level=logging.INFO)


class NoConfigException(BaseException):

    def __init__(self, victim, filepath):
        victim.logger.fatal("No fuch file as config file {}".format(filepath))
        super(NoConfigException, self).__init__()
        # sys.exit(1)

class NoAccessConfigException(BaseException):

    def __init__(self, filepath):
        logging.fatal("Can't read config file {}".format(filepath))
        super(NoAccessConfigException, self).__init__()
        # sys.exit(2)


def randomname(n):
    return "".join([random.choice(string.hexdigits) for X in range(n)])


class BaseOperator(object):
    badkeys = ("sectioname", "overseer", "predecesor")
    rootlogger = logging.getLogger()
    partA = [x.strip() for x in open("Operators/przymiotniki")]
    partB = [x.strip() for x in open("Operators/rzeczowniki")]

    def __init__(self, overseer, sectioname, conf):
        self.overseer = overseer
        self.predecesor = None
        self.sectioname = sectioname
        conf.pop("id")
        conf.pop("home")
        conf.pop("model_folder")
        conf.pop("link_folder")
        self.conf = conf


    def setpredecesor(self, predecesor):
        self.predecesor = predecesor

    def verify(self):
        if not os.path.exists(self.overseer.location):
            self.logger("Can't find location {}".format(self.overseer.location))
            sys.exit(2)
        self.outfile = os.path.join(self.overseer.workdir, self._hash)

    def run(self):
        # self.logger.info(" zrzucam do pliku {}".format(self.outfile))
        if os.path.exists(self.outfile):
            self.logger.info("My destination file exists")
            with open(self.outfile) as fw:
                try:
                    fcntl.flock(fw, fcntl.LOCK_SH | fcntl.LOCK_NB)
                except IOError:
                    self.logger.info("My destination file has EX lock")
                    fcntl.flock(fw, fcntl.LOCK_SH)
                finally:
                    fcntl.flock(fw, fcntl.LOCK_UN)
        else:
            with open(self.outfile, "w") as fw:
                try:
                    fcntl.flock(fw, fcntl.LOCK_EX)
                    self._work()
                finally:
                    fcntl.flock(fw, fcntl.LOCK_UN)

    def _run_wrapped(self, command):
        with open("", "w") as fwout, open("", "w") as fwerr:
            process = subprocess.Popen(shlex.split(command), stdout=fwout, stderr=fwerr)
            print process.returncode

    # def _work(self):
    #     self.logger.info("I did my work")

    def _makehash(self):
        m = hashlib.md5()
        self.hashelements = sorted(self.__dict__.iteritems(), key=lambda x: x[0])
        word = ''.join([''.join(map(str, x)) for x in self.hashelements if x[0] not in self.badkeys])
        if self.predecesor is not None:
            word = word + self.predecesor._hash
        m.update(word)
        self._hash = m.hexdigest()
        self._hashint = int(self._hash, 16)

    def _makename(self):
        a = self.partA[self._hashint%len(self.partA)]
        b = self.partB[self._hashint%len(self.partB)]
        self.hname = "_".join([a, b])

    def ahash(self):
        self._makehash()
        self._makename()
        self.logger = logging.getLogger(self.hname)

    def __repr__(self):
        return self._hash

    def __str__(self):
        return "{}\"{}\"".format(self.__class__.__name__, self.hname)

    def describe(self):
        proper = [" = ".join(map(str, x)) for x in self.hashelements if x[0] not in self.badkeys]
        # self.logger.info(", ".join(proper))
