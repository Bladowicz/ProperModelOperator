from BaseOperator import BaseOperator
import os
import sys
import errno
import gzip
from collections import Counter

class Predictor(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(Predictor, self).__init__(*args, **kwargs)
        try:
            self.starter = self.conf["starter"]

        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        command = self.makecommand()
        self.logger.info("[COMMAND] {}".format(command))
        self._run_wrapped(command)

    def makecommand(self):
        params = {}
        command = "{starter} -i {modelfile} -t {testdatafile} -p {predfile} --link=logistic --compressed"
        params["starter"] = self.starter
        params["modelfile"] = self._findpred("VWOperator").outfile
        params["testdatafile"] = self._findpred("Spliter").predfile
        params["predfile"] = self.outfile
        return command.format(**params)