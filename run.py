#!/usr/bin/python
import Operators as O
import os

def main():
    controler = O.ModelOperator("VWT.default.ini")
    controler.register()
    controler.verify()
    controler.summarize()
    controler.run()







if __name__ == "__main__":
    main()