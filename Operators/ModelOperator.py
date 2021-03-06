from BaseOperator import NoConfigException
import ConfigParser
from VWOperator import VWOperator
from ModelClassUpdaterOperator import MCUOperator
from TopFeatureOperator import TopFeatureOperator
from HClusterOperator import HClusterOperator
from HClusterFilterOperator import HClusterFilterOperator
from NamespaceRemapOperator import NamespaceRemapOperator
import logging

operators = {
    "vw": VWOperator,
    "mcu": MCUOperator,
    "topfeature": TopFeatureOperator,
    "remap": NamespaceRemapOperator,
    "hcluster": HClusterOperator,
    "hclustertransate": HClusterFilterOperator,

}

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
            instance = operator(self, section, **dict(self.config.items(section)))

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
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(configfile)
        _sections = [x for x in self.config.sections() if len(x.split("_")) == 2 and x.split("_")[0].isdigit()]
        self._sections = sorted(_sections, key=lambda x: int(x.split("_")[0]))
        self.name = self.config.get("main", "name")
        self.location = self.config.get("main", "file_location")
        self.logger = logging.getLogger(self.name)

    def summarize(self):
        self.logger.info(" >> ".join(map(str, self.operators)))
        for operator in self.operators:
            operator.describe()


