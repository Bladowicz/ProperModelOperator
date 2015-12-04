#!/usr/bin/python
import Operators as O
import sys


def _TMP_run(configfile):
    controler = O.ModelOperator(configfile)
    # # O.setConfigPath(startdir)

    sys.exit()

    #
    controler.verify()
    #
    # controler.run()


def main():

    _TMP_run(sys.argv[1])







if __name__ == "__main__":
    main()