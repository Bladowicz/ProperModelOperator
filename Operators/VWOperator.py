from BaseOperator import BaseOperator
import os
import sys

class VWOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(VWOperator, self).__init__(*args, **kwargs)
        try:
            self.passes = int(self.conf["passes"]) ##kwargs.pop("min_class")
            self.power_t = float(self.conf["power_t"]) ##kwargs.pop("min_class")
            self.l = self.conf["l"] ##kwargs.pop("min_class")
            self.l1 = self.conf["l1"] ##kwargs.pop("min_class")
            self.l2 = self.conf["l2"] ##kwargs.pop("min_class")
            self.hash_length = self.conf["hash_length"] ##kwargs.pop("min_class")
            self.loss_function = self.conf["loss_function"] ##kwargs.pop("min_class")
            self.cache_file = self.conf["cache_file"] ##kwargs.pop("min_class")
            self.tags = self.conf["tags"] ##kwargs.pop("min_class")
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        self.logger.info("I did my work")