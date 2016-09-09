from CalibrationTimingScanner import CalibrationTimingScanner
from ControlTimingScanner import ControlTimingScanner
from ErrorReportTimingScanner import ErrorReportTimingScanner
from MtdResultTimingScanner import MtdResultTimingScanner
from PrintedReagentTimingScanner import PrintedReagentTimingScanner

class TimingScannerManager():

    def __init__(self):
        self.REPORT_FOLDER = r'C:\A002\Reports'
        self.DATA_FOLDER = r'C:\A002\DATA'
        self.DB_PATH = r'DaAn'

        self.calibration_timing_scanner = CalibrationTimingScanner(self.REPORT_FOLDER, self.DB_PATH)
        self.control_timing_scanner = ControlTimingScanner(self.REPORT_FOLDER, self.DB_PATH)
        self.error_report_timing_scanner = ErrorReportTimingScanner(self.REPORT_FOLDER, self.DB_PATH)
        self.mtd_result_timing_scanner = MtdResultTimingScanner(self.DATA_FOLDER, self.DB_PATH)
        self.printed_reagent_timing_scanner = PrintedReagentTimingScanner(self.REPORT_FOLDER, self.DB_PATH)

    def start_all(self):
        pass

    def stop_all(self):
        pass

def test():
    TimingScannerManager()

if __name__ == "__main__":
    test()