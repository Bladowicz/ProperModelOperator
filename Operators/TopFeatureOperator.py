from BaseOperator import BaseOperator
import os
import sys

class TopFeatureOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(TopFeatureOperator, self).__init__(*args, **kwargs)
        try:

            self.minclass = int(self.conf["leave_1_every"]) ##kwargs.pop("min_class")
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        self.logger.info("I did my work")