#!/usr/bin/python
import Operators as O
import os
import sys
import multiprocessing as mp
import glob

class rabbitProccess(mp.Process):

    def __init__(self, config):
        self.config = config
        mp.Process.__init__(self)

    def run(self):
        start_rabbit(self.config)



def start_rabbit(config_file):
    controler = O.ModelOperator(config_file)
    controler.register()
    controler.verify()
    controler.summarize()
    controler.run()


# def main(location):
#     rabbits = []
#     for filename in glob.glob(os.path.join(location, "*.ini")):
#         rabbits.append(rabbitProccess(filename))
#     [rabbit.start() for rabbit in rabbits]
#     [rabbit.join() for rabbit in rabbits]





if __name__ == "__main__":
    location = os.path.abspath(sys.argv[1])
    # main(location)
    start_rabbit(os.path.join(location, sys.argv[1]))