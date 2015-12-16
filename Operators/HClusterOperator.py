from BaseOperator import BaseOperator
import os
import sys

class HClusterOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(HClusterOperator, self).__init__(*args, **kwargs)
        try:
            self.cluster_count = int(self.conf["cluster_count"]) ##kwargs.pop("min_class")
            self.ala = int(self.conf["h aha ala"].strip("h")) ##kwargs.pop("min_class")
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        self.logger.info("I did my work")