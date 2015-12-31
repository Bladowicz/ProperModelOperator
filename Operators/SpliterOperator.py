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
        self.predfile = self.outfile + ".predictionSample"
        self.pastVW = self._findpred("VWOperator")
        pC, tC, c = Counter(), Counter(), Counter()
        for nr, line in enumerate(gzip.open(self.pastVW.infile)):
            c[line[:2]] += 1
        self.linecount = nr + 1
        self.logger.info("Total count: {}, where {}".format(self.linecount, ", ".join(["{}: {}".format(k, v) for k,v in c.iteritems()])))
        self.part = (self.linecount / self.parts) * (self.parts - 1)
        with gzip.open(self.outfile, "w") as fw, gzip.open(self.predfile, "w") as fwPred:
            for nr, line in enumerate(gzip.open(self.pastVW.infile)):
                if nr <= self.part:
                    fw.write(line + "\n")
                    tC[line[:2]] += 1
                else:
                    fwPred.write(line + "\n")
                    pC[line[:2]] += 1
        self.logger.info("Training file count: {}, where {}".format(sum(tC.itervalues()),  ", ".join(["{}: {}".format(k, v) for k,v in tC.iteritems()]) ))
        self.logger.info("Prediction sample file count: {}, where {}".format(sum(pC.itervalues()), ", ".join(["{}: {}".format(k, v) for k,v in pC.iteritems()]) ))