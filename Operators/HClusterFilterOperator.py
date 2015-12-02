from BaseOperator import BaseOperator
import os
import sys


class HClusterFilterOperator(BaseOperator):

    def __init__(self,):
        super(HClusterFilterOperator, self).__init__()

    def verify(self):
        if self.predecesor.__class__.__name__ != "HClusterOperator":
            self.logger.fatal("Predecesor of HClusterFilterOperator should be HCluster")
            sys.exit(3)