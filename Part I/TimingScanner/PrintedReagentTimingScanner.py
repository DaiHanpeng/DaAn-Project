from threading import Timer

from PrintedReagentParser.PrintedReagentParser import PrintedReagentInfoParser
from DatabaseInterface.DBInterface import DBInterface

from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 60 # scan control log file time interval in seconds

class PrintedReagentTimingScanner(PrintedReagentInfoParser):
    """

    """
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        PrintedReagentInfoParser.__init__(self)
        self.timer.start()

    def timing_exec_func(self):
        #file_path = r'..\Advia2400_ScreenCapture'
        self.extract_info_from_printed_file(self.file_path)

        db_interface = DBInterface()
        try:
            db_interface.db_connect_initialize(self.db_path)
            db_interface.put_printed_reagent_info(self)
        except Exception as ex:
            print ex
        finally:
            db_interface.db_disconnect()

        # notify Part II
        rpc_client = RpcClient()
        rpc_client.fire_reagent_notification()

        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print 'timer start again'


def test():
    file_path = r'..\Advia2400_ScreenCapture'
    db_path = r'D:\DaAn\DaAn-Project\Part II\DaAn.db'
    timing_scanner = PrintedReagentTimingScanner(file_path,db_path)

if __name__ == '__main__':
    test()

