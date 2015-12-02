from BaseOperator import BaseOperator
import os


class HClusterOperator(BaseOperator):

    def __init__(self, configname):
        super(HClusterOperator, self).__init__()
        self.configpath = os.path.join(self.configpath, configname)
        self.logger.info(self.configpath)