from BaseOperator import BaseOperator
import os


class VWOperator(BaseOperator):

    def __init__(self, configname):
        super(VWOperator, self).__init__()
        self.configpath = os.path.join(self.configpath, configname)
        self.logger.info(self.configpath)