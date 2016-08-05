from threading import Timer

import sys

from GetLatestFile.GetLatestFile import GetLatestFile
from ControlParser.ControlParser import ControlParser,ControlInfo
from DatabaseInterface.MySqlInterface import DBInterface
from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 30 # scan control log file time interval in seconds

class ControlTimingScanner(ControlParser):
    """

    """
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.latest_qc_file_name = ''
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        ControlParser.__init__(self)
        #self.timer.start()
        self.timing_exec_func()

    def timing_exec_func(self):
        print 'ControlTimingScanner timing function execute start...'
        #file_path = r'..\Advia2400_ScreenCapture'
        latest_qc_file_name = GetLatestFile.get_latest_file(self.file_path,'Control_','.TXT')
        if latest_qc_file_name and self.latest_qc_file_name <> latest_qc_file_name:

            #update latest calibration file name.
            self.latest_qc_file_name = latest_qc_file_name

            self.extract_qc_info(self.file_path)

            db_interface = DBInterface()
            try:
                db_interface.db_connect_initialize(self.db_path)
                db_interface.put_control_info(self)
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


def test():
    file_path = r'C:\A002\Reports'
    db_path = r'DaAn'
    timing_scanner = ControlTimingScanner(file_path,db_path)

if __name__ == '__main__':
    test()

