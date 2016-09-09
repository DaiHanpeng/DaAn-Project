from threading import Timer

from CalibrationCurveParser.CalibrationCurveParser import CalibrationCurveParser
from DatabaseInterface.MySqlInterface import DBInterface
from GetLatestFile.GetLatestFile import GetLatestFile

from RpcInterface.RpcClient import RpcClient

FILE_SCAN_INTERVAL = 60 # scan control log file time interval in seconds

class CalibrationCurveTimingScanner(CalibrationCurveParser):
    '''

    '''
    def __init__(self,file_path,db_path):
        self.file_path = file_path
        self.db_path = db_path
        self.latest_cal_file_name = ''
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        CalibrationCurveParser.__init__(self)
        #self.timer.start()
        self.timing_exec_func()

    def timing_exec_func(self):
        print 'CalibrationCurveTimingScanner timing function execute start...'
        #file_path = r'..\Advia2400_ScreenCapture'
        latest_cal_file_name = GetLatestFile.get_latest_file(self.file_path,'Calibration Curve','.TXT')
        if latest_cal_file_name and self.latest_cal_file_name <> latest_cal_file_name:

            #update latest calibration file name.
            self.latest_cal_file_name = latest_cal_file_name

            self.extract_cal_info(self.file_path)

            db_interface = DBInterface()
            try:
                db_interface.db_connect_initialize(self.db_path)
                db_interface.put_calibration_curve_info(self)
            except Exception as ex:
                print ex
            finally:
                db_interface.db_disconnect()

            # notify Part II
            rpc_client = RpcClient()
            rpc_client.fire_calibration_curve_notification()

            print self

        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print 'timer start again'

def test():
    file_path = r'C:\A002\Reports'
    db_path = r'DaAn'
    CalibrationCurveTimingScanner(file_path,db_path)

if __name__ == '__main__':
    test()
