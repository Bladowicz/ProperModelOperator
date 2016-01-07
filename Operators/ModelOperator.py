from BaseOperator import NoConfigException
import ConfigParser
from VWOperator import VWOperator
from ModelClassUpdaterOperator import MCUOperator
from TopFeatureOperator import TopFeatureOperator
from HClusterOperator import HClusterOperator
from HClusterFilterOperator import HClusterFilterOperator
from NamespaceRemapOperator import NamespaceRemapOperator
from TimeDelta import TimeDelta
from Linker import Linker
from SpliterOperator import Spliter
from Predictor import Predictor
import logging
import sys
import os

class opDict(dict):
    def __missing__(self, key):
        logging.fatal("Bad operator name : \"{}\"".format(key))
        logging.fatal("Proper opperators {}".format(", ".join(sorted(self.iterkeys()))))
        sys.exit(12)
        return

operators = opDict()
operators["vw"] = VWOperator
operators["mcu"] = MCUOperator
operators["topfeature"] = TopFeatureOperator
operators["remap"] = NamespaceRemapOperator
operators["hcluster"] = HClusterOperator
operators["hclustertransate"] = HClusterFilterOperator
operators["time"] = TimeDelta
operators["link"] = Linker
operators["spliter"] = Spliter
operators["predict"] = Predictor



class ModelOperator(object):



    def __init__(self, configfile):
        self.operators = []
        self.tempfiles = []
        self.configfile = configfile
        self._readconfig(self.configfile)

    # @ModelOperatorErrors
    def register(self):
        for section in self._sections:
            operator = operators[section.split("_")[1]]
            instance = operator(self, section, dict(self.config.items(section)))
            if len(self.operators) > 0:
                instance.setpredecesor(self.operators[-1])
            self.operators.append(instance)

    def verify(self):
        for operator in self.operators:
            operator.ahash()
            operator.verify()


    def run(self):
        for operator in self.operators:
            operator.run()

    def _checkconfigfile(self, configfile):
        pass

    def _readconfig(self, configfile):
        self._checkconfigfile(configfile)
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.read(configfile)
        _sections = [x for x in self.config.sections() if len(x.split("_")) == 2 and x.split("_")[0].isdigit()]
        self._sections = sorted(_sections, key=lambda x: int(x.split("_")[0]))
        self.name = self.config.get("main", "name")
        self.location = self.config.get("main", "file_location")
        self.workdir = self.config.get("main", "work_location")
        logger = logging.getLogger(self.name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s [%(name)-12s] [%(levelname)-6s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.propagate = False
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        #
        self.logger = logger
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
            self.logger.warn("Workdir {} did not exist, so it was created.".format(self.workdir))

    def summarize(self):
        self.logger.info(" >> ".join(map(str, self.operators)))
        for operator in self.operators:
            operator.describe()


