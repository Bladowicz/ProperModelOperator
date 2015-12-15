from BaseOperator import BaseOperator
import os
import sys

class TopFeatureOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        try:
            self.src = kwargs.pop("src")
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)
        super(TopFeatureOperator, self).__init__(*args, **kwargs)
