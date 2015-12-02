#!/usr/bin/python
import Operators as O


def main():
    controler = O.ModelOperator()
    O.setConfigPath("/home/gbaranowski/etc")
    controler.register(O.MCUOperator, "some1.ini")
    controler.register(O.TopFeatureOperator, "some2.ini")
    controler.register(O.HClusterOperator, "some3.ini")
    controler.register(O.HClusterFilterOperator)
    controler.register(O.VWOperator, "some4.ini")
    #
    controler.verify()
    #
    # controler.run()








if __name__ == "__main__":
    main()