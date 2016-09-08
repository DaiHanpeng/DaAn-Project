import clr
from System import DateTime

from DBTables import *

class InsCalibrationStatusHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsCalibrationStatus(cursor):
        unsent_ins_cal_status = []
        if cursor:
            cursor.execute("SELECT * FROM InsCalibrationStatus WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                cal = ins_calibration_status()
                cal.Curve = row['Curve']
                cal.FitRate = row['FitRate']
                cal.LotNo = row['LotNo']
                cal.ReagentLotNo = row['ReagentLotNo']
                cal.ResultDate = DateTime.Parse(row['ResultDate'])
                
                cal.State = CalibrationStateType.Unkown
                if 'Pass' == row['State']:
                    cal.State = CalibrationStateType.Pass
                elif 'Fail' == row['State']:
                    cal.State = CalibrationStateType.Failed
                cal.TestCode = row['TestCode']
                cal.TtlNums = int(row['TtlNums'])
                cal.Sent = row['Sent']
                cal.ID = row['ID']
                cal.uuid = row['uuid']

                unsent_ins_cal_status.append(cal)
        return unsent_ins_cal_status

    @staticmethod
    def set_InsCalibrationStatus_as_sent(ins_cal_status,cursor,connect):
        for cal_status in ins_cal_status:
            if cursor and connect and isinstance(cal_status,ins_calibration_status):
                cursor.execute("UPDATE InsCalibrationStatus SET Sent = 1 WHERE ID = {0}".format(cal_status.ID))
                connect.commit()


