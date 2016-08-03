from threading import Timer

import sys

from GetLatestFile.GetLatestFile import GetLatestFile
from ErrorReportParser.ErrorReportParser import ErrorReportParser
from DatabaseInterface.DBInterface import DBInterface
from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 30 # scan control log file time interval in seconds

class ErrorReportTimingScanner(ErrorReportParser):
    """
    timing exe of Error Report Scann.
    """
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.latest_err_report_file_name = r''
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        ErrorReportParser.__init__(self)
        #self.timer.start()
        self.timing_exec_func()

    def timing_exec_func(self):
        print 'ErrorReportParser timing function execute start...'
        #file_path = r'.'
        latest_err_report_file_name = GetLatestFile.get_latest_file(self.file_path,'Error_','.TXT')
        if latest_err_report_file_name and self.latest_err_report_file_name <> latest_err_report_file_name:

            #update latest error report file name.
            self.latest_err_report_file_name = latest_err_report_file_name

            self.extract_error_report_info(self.file_path)

            db_interface = DBInterface()
            try:
                db_interface.db_connect_initialize(self.db_path)
                db_interface.put_instrument_status_info(self)
                db_interface.put_instrument_log_info(self)
            except Exception as ex:
                print ex
            finally:
                db_interface.db_disconnect()

            # notify Part II
            rpc_client = RpcClient()
            rpc_client.fire_control_notification()

            print self

        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print 'timer start again'



