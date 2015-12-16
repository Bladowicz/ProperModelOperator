import os
import sys
import logging

from BaseOperator import BaseOperator


class MCUOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(MCUOperator, self).__init__(*args, **kwargs)
        try:
            self.sclass = self.conf["success_class"]
            self.starter = self.conf["starter"]# kwargs.pop("starter")
            self.minclass = int(self.conf["min_class"]) ##kwargs.pop("min_class")
            self.eventlog = self.conf["event log location"]
            self.countries = self.conf["countries"]
            self.timestamp = self.conf["timestamp"]
            self.namespacemap = self.conf["namespacemap"]
            self.parameters = self.conf["parameters"]

        except KeyError as e:
            self.rootlogger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)


    def _work(self):

        self.logger.info("[COMMAND] "+ self.makecommand())

    def makecommand(self):
        options = {}
        command = "{starter} {eventlog} {outfile} {successclass} {minclass} {mintimestamp} {namespace} {countries} {parameters}"
        options["starter"] = self.starter
        options["eventlog"] = "" if self.eventlog == "" else "-e {}".format(self.eventlog)
        options["outfile"] = "" if self.outfile == "" else "-o {}".format(self.outfile)
        options["successclass"] = "" if self.sclass == "" else "-C {}".format(self.sclass)
        options["minclass"] = "" if self.minclass == "" else "-m {}".format(self.minclass)
        options["mintimestamp"] = "" if self.timestamp == "" else "-t {}".format(self.timestamp)
        options["namespace"] = "" if self.namespacemap == "" else "-t {}".format(self.namespacemap)
        options["countries"] = "" if self.countries == "" else "-c {}".format(self.countries)
        options["parameters"] = " ".join(map(lambda x: "--" + x, self.parameters))
        return command.format(**options)