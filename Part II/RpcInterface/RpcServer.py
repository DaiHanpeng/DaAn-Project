#import xmlrpclib

import sys
import clr
'''
clr.AddReferenceToFileAndPath(r'C:\Program Files (x86)\IronPython 2.7')
clr.AddReferenceToFileAndPath(r'C:\Program Files (x86)\IronPython 2.7\DLLs')
clr.AddReferenceToFileAndPath(r'C:\Program Files (x86)\IronPython 2.7\Lib')
clr.AddReferenceToFileAndPath(r'C:\Program Files (x86)\IronPython 2.7\Lib\site-packages')
'''
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\DLLs')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')


from SimpleXMLRPCServer import SimpleXMLRPCServer

from DBInterface.DBTables import *
from DBInterface.SqliteInterface import SqliteInterface
from DaAnInterface.DaAnInterface import DaAnInterface


class MessageHandler():
    """
    """
    def __init__(self):
        pass

    def reagent_handler(self):
        print 'reagent handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                reagents = db_interface.fetch_unsent_items_from_InsReagentInfo()
                if reagents:
                    ##
                    print 'get unsent ins reagent info records,'
                    for reagent in reagents:
                        if isinstance(reagent,ins_reagent_info):
                            print reagent
                    ## reagent info processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_reagent_info(reagents)
                    ##
                    db_interface.set_InsReagentInfos_as_sent(reagents)

                    print 'reagent info processing finished successfully...'
            except Exception as ex:
                print ex

    def order_result_handler(self):
        print 'order result handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                tests = db_interface.fetch_unsent_items_from_InsTest()
                if tests:
                    ##
                    print 'get unsent ins test info records,'
                    for test in tests:
                        if isinstance(test,ins_test):
                            print test
                    ## reagent info processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_order_result_info(tests)
                    ##
                    db_interface.set_InsTests_as_sent(tests)

                    print 'patient result processing finished successfully...'
            except Exception as ex:
                print ex

    def calibration_handler(self):
        print 'calibration result handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                cal_results = db_interface.fetch_unsent_items_from_InsCalibrationResult()
                if cal_results:
                    ##
                    print 'get unsent ins calibration results info records,'
                    for result in cal_results:
                        if isinstance(result,ins_calibration_result):
                            print result
                    ## calibration result processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_calibration_result(cal_results)
                    ##
                    db_interface.set_InsCalibrationResults_as_sent(cal_results)

                    print 'calibration result processing finished successfully...'
            except Exception as ex:
                print ex

    def control_handler(self):
        print 'qc result handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                qc_results = db_interface.fetch_unsent_items_from_InsQC()
                if qc_results:
                    ##
                    print 'get unsent ins qc results info records,'
                    for result in qc_results:
                        if isinstance(result,ins_qc):
                            print result
                    ## qc result processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_qc_result(qc_results)
                    ##
                    db_interface.set_InsQCs_as_sent(qc_results)

                    print 'control result processing finished successfully...'
            except Exception as ex:
                print ex

def test():
    server = SimpleXMLRPCServer(("localhost", 8000),allow_none=True)
    server.register_introspection_functions()
    server.register_instance(MessageHandler())
    server.serve_forever()
    input('should not be here ...')

if __name__  == '__main__':
    test()
