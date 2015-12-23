from BaseOperator import BaseOperator
import os
import sys
import errno
import gzip
from collections import Counter

class Spliter(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(Spliter, self).__init__(*args, **kwargs)
        try:
            self.parts = int(self.conf["parts"])



        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        self.pastVW = self._findpred("VWOperator")
        c = Counter()
        i = 0
        for nr, line in enumerate(gzip.open(self.pastVW.infile)):
            c[line[:2]] += 1
        self.classes = c + 1
        self.linecount = nr
        self.logger.info("Total count: {}, where {}".format(nr, ", ".join(["{}: {}".format(k, v) for k,v in c.iteritems()])))

