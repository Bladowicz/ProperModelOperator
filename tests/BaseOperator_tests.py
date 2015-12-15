from nose.tools import *
import Operators.BaseOperator as BO
from Operators.BaseOperator import NoConfigException, NoAccessConfigException
import os

def setup():
    """aaaa"""
    print "SETUP!"

def teardown():
    """bbbbb"""
    print "TEAR DOWN!"


@raises(NoConfigException)
def test_NoConfig():
    """ No config file causes NoConfigException """
    b = BO()
    b._loadconfig("")

def setup_NoConfig():
    open('test.txt', 'w').close()
    os.chmod('test.txt', 0)

def teardown_NoConfig():
    os.chmod("test.txt", 7)
    os.remove("test.txt")

@with_setup(setup_NoConfig, teardown_NoConfig)
@raises(NoAccessConfigException)
def test_NoConfigPermissions():
    """ No read permission for config causes NoAccessConfigException """
    b = BO()
    b._loadconfig("test.txt")



