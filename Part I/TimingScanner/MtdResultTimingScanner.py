from threading import Timer
import os

from MtdResultInfoParser.MtdResultParser import MtdResultParser
from DatabaseInterface.DBInterface import DBInterface

from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 60 # scan control log file time interval in seconds

class MtdResultTimingScanner(MtdResultParser):
    """

    """
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        MtdResultParser.__init__(self)
        #self.timer.start()
        self.timing_exec_func()

    def timing_exec_func(self):
        #file_path = r'..\Advia2400_ScreenCapture'
        print 'timer handler started.'
        if os.path.exists(self.file_path):
            try:
                self.build_result_info_from_mtd_file(self.file_path)
                print r'#1'
            except Exception as ex:
                print ex

            db_interface = DBInterface()
            try:
                print r'#2'
                db_interface.db_connect_initialize(self.db_path)
                db_interface.put_mtd_result_info(self)

                # notify Part II
                rpc_client = RpcClient()
                rpc_client.fire_order_result_notification()
            except Exception as ex:
                print ex
            finally:
                db_interface.db_disconnect()

            print r'#3'
            self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
            self.timer.start()
            print self
            print 'MtdResultTimingScanner timer start again'
        else:
            print 'mtd file not exists...'


def test():
    file_path = r'D:\DaAn\DaAn-Project\Part I\A002\DATA'
    db_path = r'D:\DaAn\DaAn-Project\Part II\DaAn.db'
    timing_scanner = MtdResultTimingScanner(file_path,db_path)

if __name__ == '__main__':
    test()

