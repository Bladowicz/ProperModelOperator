import os
import sys
import logging

from BaseOperator import BaseOperator


class MCUOperator(BaseOperator):


    def __init__(self, *args, **kwargs):

        try:
            self.sclass = kwargs.pop("sclass")
            self.minclass = int(kwargs.pop("minclass"))
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)
        super(MCUOperator, self).__init__(*args, **kwargs)
        # self._badconfig(kwargs)

    def run(self):
        command = "echo hello world"
        # self._run_wrapped(command)