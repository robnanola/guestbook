#!/usr/bin/python

import optparse
import sys
import os
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


class StopFile():

    def __init__(self):
        self.filename = 'stop'
        self.init_file()
        

    def writeToFile(self, obj):
        """
        accepts string or list to be written to file. 
        usually used to log error results from tests to stop auto deploy.
        """

        f = open(self.filename,'a')

        if type(obj) == str:
            f.write(obj)
        elif type(obj) == list:
            for i in obj:
                f.write(str(i))
        f.close()


    def init_file(self):
        f = open(self.filename,'w')
        f.close()

    def is_empty(self):

        if os.stat(self.filename).st_size == 0:
            return True
        return False



def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    stopfile = StopFile()

    suite = unittest.loader.TestLoader().discover(test_path)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

    if test_result.wasSuccessful() == False:
        stopfile.writeToFile(test_result.failures)
    else:
        # upload/deploy file 
        os.system("appcfg.py update .")



if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print 'Error: Exactly 2 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    main(SDK_PATH, TEST_PATH)
