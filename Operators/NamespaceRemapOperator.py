from BaseOperator import BaseOperator
import os


class NamespaceRemapOperator(BaseOperator):

    def __init__(self, configname):
        super(NamespaceRemapOperator, self).__init__()
        self.configpath = os.path.join(self.configpath, configname)
        self.logger.info(self.configpath)