from BaseOperator import BaseOperator
import os


class TopFeatureOperator(BaseOperator):

    def __init__(self, configname):
        super(TopFeatureOperator, self).__init__()
        self.configpath = os.path.join(self.configpath, configname)
        self.logger.info(self.configpath)