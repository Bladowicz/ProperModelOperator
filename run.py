#!/usr/bin/python
import Operators as O


def main():
    controler = O.ModelOperator("/home/gbaranowski/etc/VWT/model2.ini")
    controler.register()
    controler.verify()
    controler.summarize()
    controler.run()







if __name__ == "__main__":
    main()