from BaseOperator import NoConfigException
import ConfigParser
import os
from BaseOperator import BaseOperator
from ModelClassUpdaterOperator import MCUOperator
from VWOperator import VWOperator
from TopFeatureOperator import TopFeatureOperator
from HClusterOperator import HClusterOperator
from HClusterFilterOperator import HClusterFilterOperator

# def ModelOperatorErrors(fun):
#
#     def wrapper(*args, **kwargs):
#         try:
#             out = fun(*args, **kwargs)
#             return out
#         except NoConfigException:
#             wrapper.called += 1
#             return None
#     wrapper.called = 0
#     wrapper.__name__ = fun.__name__
#     return wrapper


def CheckInputFile(fun):

    def wrapper(self, filename, *args, **kwargs):
        print filename
        if not os.path.exists(filename):
            raise ## ToDo
        if not os.access(filename, 4):
            raise ## ToDo

        out = fun(self, filename, *args, **kwargs)
        return out

    wrapper.__name__ = fun.__name__
    return wrapper


class ModelOperator(object):
    nametooperator = {"mcupdater":MCUOperator,
                 "topfeature":TopFeatureOperator,
                 "hclutstering":HClusterOperator,
                 "hctranslation":HClusterFilterOperator,
                 "vowpal":VWOperator,
    }

    def __init__(self, configfile):
        self.operators = []
        self.tempfiles = []
        self._readconfig(configfile)

    @CheckInputFile
    def _readconfig(self, config):
        parser = ConfigParser.SafeConfigParser()
        parser.read(config)
        sections = [x.split("_") for x in parser.sections()]
        ops = map(lambda x: (int(x[0]), self.nametooperator[x[1]], "_".join(x)), [x for x in sections if len(x) == 2])
        ops = sorted(ops, key=lambda x: x[0])
        for o in ops:
            self.register(o[1](o[0], **dict(parser.items(o[2]))))


    # @ModelOperatorErrors
    def register(self, operator):
        if len(self.operators) > 0:
            operator.setpredecesor(self.operators[-1])
        self.operators.append(operator)

    def verify(self):
        for operator in self.operators:
            operator.verify()

    def run(self):
        for operator in self.operators:
            operator.run()