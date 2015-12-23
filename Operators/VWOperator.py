from BaseOperator import BaseOperator
import os
import sys

def optionalize(formatingString, value):
    return "" if value == "" else formatingString.format(value)

class VWOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(VWOperator, self).__init__(*args, **kwargs)
        try:
            self.starter = self.conf["starter"]
            self.passes = int(self.conf["passes"]) ##kwargs.pop("min_class")
            self.power_t = float(self.conf["power_t"]) ##kwargs.pop("min_class")
            self.l = self.conf["l"] ##kwargs.pop("min_class")
            self.l1 = self.conf["l1"] ##kwargs.pop("min_class")
            self.l2 = self.conf["l2"] ##kwargs.pop("min_class")
            self.hash_length = self.conf["hash_length"] ##kwargs.pop("min_class")
            self.loss_function = self.conf["loss_function"] ##kwargs.pop("min_class")
            self.tags = self.conf["tags"].split(",") ##kwargs.pop("min_class")
            self.ignored = self.conf["ignored"]
        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)

    def _work(self):
        self.cache_file = self.outfile + ".cache"
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        command = self.makecommand(self.predecesor.outfile)
        self.logfile = self.outfile + ".log"
        last_mcu = self._findpred("MCUOperator")
        self.logger.info("LAST MCU PARAMS "+ " ".join(last_mcu.parameters))
        if "gzip" in last_mcu.parameters:
            self.logger.info("MCU had gzip")
            if "compressed" not in self.tags:
                self.logger.info("VW compressed added")
                self.tags.append("compressed")
        self.logger.info("[COMMAND] {}".format(command))
        self._run_wrapped(command)

    def makecommand(self, infile):
        options = {}
        command = "{starter} {infile} -f {outfile} {loss_function} {hash_length} {l2} {l1} {l} {power_t} {passes} {tags} {cache_file} {ignore}"
        options["starter"] = self.starter
        options["infile"] = infile
        options["outfile"] = self.outfile
        options["loss_function"] = optionalize("--loss_function {}", self.loss_function)
        options["hash_length"] = optionalize("-b {}", self.hash_length)
        options["l"] = optionalize("-l {}", self.l)
        options["l1"] = optionalize("--l1 {}", self.l1)
        options["l2"] = optionalize("--l2 {}", self.l2)
        options["ignore"] = optionalize("--ignore {}", self.ignored)
        options["power_t"] = optionalize("--power_t {}", self.power_t)
        options["passes"] = optionalize("--passes {}", self.passes)
        options["tags"] = " ".join(["--" + X for X in self.tags])
        options["cache_file"] = optionalize("--cache_file {}", self.cache_file)
        return command.format(**options)

