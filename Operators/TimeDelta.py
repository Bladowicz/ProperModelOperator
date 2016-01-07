import os
import sys
import logging
import datetime
import glob


from BaseOperator import BaseOperator




class TimeDelta(BaseOperator):

    periods = ["months", "days", "hours", "minutes", "seconds"]
    period = ["month", "day", "hour", "minute", "second"]
    translate = {"s":-1, "m":-2, "h":-3, "d":-4}
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

    def __init__(self, *args, **kwargs):
        super(TimeDelta, self).__init__(*args, **kwargs)
        try:
            self.calculationmethod = self.conf["calculate by"]
            self.start = self.conf["start"]# kwargs.pop("starter")
            self.stop = self.conf["stop"] ##kwargs.pop("min_class")
            self.buffer = self.conf["buffer"]
            self.delta = self.conf["delta"]
            self.buffer = self.conf["buffer"]
            self.accuracy = self.conf["accuracy"]
            self.pattern = self.conf["filepattern"]
            if self.calculationmethod == "delta":
                self._calculatebydelta()
            elif self.calculationmethod == "range":
                self._calculatebyrange()
            else:
                logging.fatal("Bad calculation method")
                sys.exit(127)
            self.files = self._findfiles()
            self.filecount = len(self.files)
            if self.filecount ==0:
                self.logger.fatal("No files found in {}".format(self.overseer.location))
                sys.exit(128)
            else:
                self.size = sum([os.path.getsize(x) for x in self.files])



        except KeyError as e:
            self.logger.fatal("In config section {} there is no value for {}".format(self.sectioname, str(e)))
            sys.exit(1)


    def _work(self):

        self.logger.info("[COMMAND] "+ self.makecommand())

    def _calculatebydelta(self):
        now = self._makenow()
        delta = self._consumedelta()

        self.od = now - delta
        self.do = now

    def _calculatebyrange(self):
        self.od = self._stringtodate(self.start)
        self.do = self._stringtodate(self.stop)


    def makecommand(self):
        options = {}
        command = "{starter} {eventlog} {outfile} {successclass} {minclass} {mintimestamp} {namespace} {countries} {parameters}"
        return command

    @staticmethod
    def _stringtodate(date):
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    def _consumedelta(self):
        try:
            mark = self.delta[-1]
            value = int(self.delta[:-1])
            out = {self.periods[self.translate[mark]]:value}

            delta = datetime.timedelta(**out)
            return delta
        except Exception as e:
            logging.fatal("Bad delta value '{}' - {}".format(self.delta, str(e)))
            raise

    def _makenow(self):
        now = datetime.datetime.now()
        now = self._setaccuracy(now)
        now = self._consumebuffer(now)
        return now

    def _consumebuffer(self, now):
        try:
            mark = self.buffer[-1]
            value = int(self.buffer[:-1])
            out = {self.periods[self.translate[mark]]:value}
            delta = datetime.timedelta(**out)
            return now - delta
        except IndexError:
            pass
        except Exception as e:
            self.logger.fatal("Bad buffer - {} : {}".format(self.buffer, str(e)))
            raise
        return now

    def _setaccuracy(self, now):
        i = self.translate.get(self.accuracy, 0)
        para = {"microsecond":0}
        while True:
            if i == 0:
                break
            para[self.period[i]] = 0
            i += 1
        return now.replace(**para)

    def verify(self):
        pass


    def run(self):
        self.logger.info("Looking for files between {} and {}".format(self.od, self.do))

        self.logger.info("Found {} files with total size {}.".format(self.filecount, self.humansize(self.size)))

    def _findfiles(self):
        pattern = self.pattern.replace("%Y", "[0-9]"*4).replace("%m", "[0-9]"*2).replace("%d", "[0-9]"*2).replace("%H", "[0-9]"*2)

        files = glob.glob(os.path.join(self.overseer.location, pattern))
        # self.overseer.logger.info("Hello {}".format())#
        return sorted(filter(self.dateFilter ,files))

    def dateFilter(self, filepath):
        filename = os.path.basename(filepath)
        d = datetime.datetime.strptime(filename, self.pattern)
        return self.od <= d <= self.do

    def humansize(self, nbytes):
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(self.suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, self.suffixes[i])