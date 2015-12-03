import os

from BaseOperator import BaseOperator


class MCUOperator(BaseOperator):

    def __init__(self, configname):
        super(MCUOperator, self).__init__()
        self.configpath = os.path.join(self.configpath, configname)
        self.logger.info(self.configpath)
        self.config = self._loadconfig(self.configpath)

    def run(self):
        command = "echo hello world"
        self._run_wrapped(command)