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
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib\site-packages')


from SimpleXMLRPCServer import SimpleXMLRPCServer

from DBInterface.DBTables import *
from DBInterface.MySqlInterface import MySqlInterface
from DaAnInterface.DaAnInterface import DaAnInterface


class MessageHandler():
    """
    """
    def __init__(self):
        pass

    def reagent_handler(self):
        print 'reagent handler is triggered...'
        with MySqlInterface() as db_interface:
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

                    print 'reagent info processing finished successfully...'+str((reagents))
            except Exception as ex:
                print ex

    def order_result_handler(self):
        print 'order result handler is triggered...'
        with MySqlInterface() as db_interface:
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

                    print 'patient result processing finished successfully...'+str(len(tests))
            except Exception as ex:
                print ex

    def calibration_curve_handler(self):
        print 'calibration curve handler is triggered...'
        with MySqlInterface() as db_interface:
            try:
                cal_status = db_interface.fetch_unsent_items_from_InsCalibrationStatus()
                if cal_status:
                    ##
                    print 'get unsent ins calibration status info records,'
                    for status in cal_status:
                        if isinstance(status,ins_calibration_status):
                            #print status
                            result_list = []
                            result_list = db_interface.fetch_unsent_items_from_InsCalibrationResult_by_uuid(status.uuid)
                            if not result_list:
                                result_list = []
                            ## calibration status processing...
                            
                            daan_result_list = []
                            for result in result_list:
                                if isinstance(result,ins_calibration_result):
                                    daan_result = InsCalibrationResult()
                                    daan_result.Absorbance = result.Absorbance
                                    daan_result.Barcode = result.Barcode
                                    daan_result.LotNo = result.LotNo
                                    daan_result.Name = result.Name
                                    daan_result.OpenDate = result.OpenDate
                                    daan_result.OpenValidDays = result.OpenValidDays
                                    daan_result.ReagentLotNo = result.ReagentLotNo
                                    daan_result.ResultDate = result.ResultDate
                                    daan_result.ResultValue = result.ResultValue
                                    daan_result.TestCode = result.TestCode
                                    daan_result.Unit = result.Unit
                                    #daan_result_list.append(daan_result)
                                    status.calibrationResults.Add(daan_result)
                            print 'status: '
                            print status
                            daan_interface = DaAnInterface()
                            daan_interface.send_one_calibration_curve(status)
                            ##
                            db_interface.set_InsCalibrationResults_as_sent_by_uuid(status.uuid)
                        db_interface.set_InsCalibrationStatus_as_sent(cal_status)
                    print 'calibration curve processing finished successfully...'+str(len(cal_status))
            except Exception as ex:
                print ex

    def calibration_handler(self):
        print 'calibration result handler is triggered...'
        with MySqlInterface() as db_interface:
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

                    print 'calibration result processing finished successfully...'+str(len(cal_results))
            except Exception as ex:
                print ex

    def control_handler(self):
        print 'qc result handler is triggered...'
        with MySqlInterface() as db_interface:
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

                    print 'control result processing finished successfully...'+str(len(qc_results))
            except Exception as ex:
                print ex

    def instrument_log_handler(self):
        print 'instrument log handler is triggered...'
        with MySqlInterface() as db_interface:
            try:
                instr_logs = db_interface.fetch_unsent_items_from_InsLog()
                if instr_logs:
                    ##
                    print 'get unsent ins log info records,'
                    for item in instr_logs:
                        if isinstance(item,ins_log):
                            print item
                    ## instrument log processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_instrument_log(instr_logs)
                    ##
                    db_interface.set_InsLogs_as_sent(instr_logs)

                    print 'instrument log processing finished successfully...'+str(len(instr_logs))
            except Exception as ex:
                print ex

    def instrument_status_handler(self):
        print 'instrument status handler is triggered...'
        with MySqlInterface() as db_interface:
            try:
                instr_status = db_interface.fetch_unsent_items_from_InsStatus()
                if instr_status:
                    ##
                    print 'get unsent ins status info records,'
                    for item in instr_status:
                        if isinstance(item,ins_status):
                            print item
                    ## instrument log processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_instrument_status(instr_status)
                    ##
                    db_interface.set_InsStatus_as_sent(instr_status)

                    print 'instrument status processing finished successfully...'+str(len(instr_status))
            except Exception as ex:
                print ex


def test():
    server = SimpleXMLRPCServer(("", 17788),allow_none=True)
    #server = SimpleXMLRPCServer(("10.10.10.200", 8000),allow_none=True)
    server.register_introspection_functions()
    server.register_instance(MessageHandler())
    server.serve_forever()
    input('should not be here ...')

if __name__  == '__main__':
    test()
