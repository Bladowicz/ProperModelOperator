from BaseOperator import BaseOperator
import os
import sys


class HClusterFilterOperator(BaseOperator):

    def __init__(self,):
        super(HClusterFilterOperator, self).__init__()
        try:
            #self.minclass = int(self.conf["leave_1_every"]) ##kwargs.pop("min_class")
            pass
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def verify(self):
        if self.predecesor.__class__.__name__ != "HClusterOperator":
            self.logger.fatal("Predecesor of HClusterFilterOperator should be HCluster")
            sys.exit(3)