from BaseOperator import BaseOperator
import os
import sys
import errno

class Linker(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(Linker, self).__init__(*args, **kwargs)
        try:
            self.location = self.conf["location"]

        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    @staticmethod
    def force_symlink(file1, file2):
        try:
            os.symlink(file1, file2)
        except OSError, e:
            if e.errno == errno.EEXIST:
                os.remove(file2)
                os.symlink(file1, file2)
            if e.errno == errno.ENOENT:
                if not os.path.exists(file1):
                    sys.exit(123)
                if not os.path.exists(file2):
                    directory = os.path.dirname(file2)
                    os.makedirs(directory)
                    os.symlink(file1, file2)
        except Exception as e:
            raise

    def _work(self):
        pred = self._findpred("VWOperator")

        self.logger.info("Linking {} to {}".format(pred.outfile, self.location))
        self.force_symlink(pred.outfile, self.location)