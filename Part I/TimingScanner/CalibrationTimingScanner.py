from threading import Timer

from CalibrationParser.CalibrationParser import CalibrationParser
from DatabaseInterface.DBInterface import DBInterface
from GetLatestFile.GetLatestFile import GetLatestFile

from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 30 # scan control log file time interval in seconds

class CalibrationTimingScanner(CalibrationParser):
    """

    """
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.latest_cal_file_name = ''
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        CalibrationParser.__init__(self)
        #self.timer.start()
        self.timing_exec_func()

    def timing_exec_func(self):
        print 'CalibrationTimingScanner timing function execute start...'
        #file_path = r'..\Advia2400_ScreenCapture'
        latest_cal_file_name = GetLatestFile.get_latest_file(self.file_path,'Calibration_','.TXT')
        if latest_cal_file_name and self.latest_cal_file_name <> latest_cal_file_name:

            #update latest calibration file name.
            self.latest_cal_file_name = latest_cal_file_name

            self.extract_cal_info(self.file_path)

            db_interface = DBInterface()
            try:
                db_interface.db_connect_initialize(self.db_path)
                db_interface.put_calibration_info(self)
            except Exception as ex:
                print ex
            finally:
                db_interface.db_disconnect()

            # notify Part II
            rpc_client = RpcClient()
            rpc_client.fire_calibration_notification()

            print self

        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print 'timer start again'


def test():
    file_path = r'..\Advia2400_ScreenCapture\Calibration'
    db_path = r'D:\DaAn\DaAn-Project\Part II\DaAn.db'
    timing_scanner = CalibrationTimingScanner(file_path,db_path)

if __name__ == '__main__':
    test()

