#!/usr/bin/python
import Operators as O
import os
import sys


def main(config_file):
    controler = O.ModelOperator(config_file)
    controler.register()
    controler.verify()
    controler.summarize()
    controler.run()







if __name__ == "__main__":
    main(sys.argv[1])