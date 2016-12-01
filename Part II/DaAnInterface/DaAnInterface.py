# -*- coding: utf-8 -*-
import sys,os
import datetime
import clr

sys.path.append(os.path.abspath('..'))

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System')
clr.AddReferenceToFile('log4net.dll')
clr.AddReferenceToFile('Google.ProtocolBuffers.dll')
clr.AddReferenceToFile('Daan.Instrument.Log.dll')
clr.AddReferenceToFile('Daan.Instrument.Connector.dll')
clr.AddReferenceToFile('IronPython.SQLite.dll')

from System.Windows.Forms import Application, Button, Form
from System.Drawing import Point
from System import *

from Daan.Instrument.Connector import *
from Daan.Instrument.Entity import *
from Daan.Instrument.Type import *
from Daan.Instrument.Connector.Common import *

from DBInterface.DBTables import *
#from DBInterface.DBInterface import DBInterface


class DaAnInterface():
    """
    """
    def __init__(self):
        pass
        #self.instrument_connector = InsConnector()

    def send_reagent_info(self,reagent_list):
        if reagent_list:
            ins_reagent_status = InsReagentStatus()
            ins_reagent_status.RunDate = DateTime.Now#datetime.datetime.now()
            ins_reagent_info_list = []
            for reagent in reagent_list:
                if isinstance(reagent,ins_reagent_info):
                    ins_reagent_info_list.append(reagent)
            #send 
            try:
                InsConnector.SendReagentStatus(ins_reagent_status,Array[InsReagentInfo](ins_reagent_info_list))
            except Exception as ex:
                print 'exception encounteered during sending reagent status... ', ex

    def send_order_result_info(self,order_result_list):
        if order_result_list:
            for test in order_result_list:
                if isinstance(test,ins_test):
                    try:
                        InsConnector.SendTest(test)
                    except Exception as ex:
                        print ex

    def send_one_calibration_curve(self,cal_status):
        if cal_status and isinstance(cal_status,ins_calibration_status):
            try:
                InsConnector.SendCalibrationResult(cal_status)
            except Exception as ex:
                print ex

    def send_calibration_result(self,cal_results):
        if cal_results:
            for result in cal_results:
                if isinstance(result,ins_calibration_result):
                    try:
                        InsConnector.SendCalibrationResult(result)
                    except Exception as ex:
                        print ex

    def send_qc_result(self,qc_results):
        if qc_results:
            for qc in qc_results:
                if isinstance(qc,ins_qc):
                    try:
                        InsConnector.SendQC(qc)
                    except Exception as ex:
                        print ex  
                        
    def send_instrument_log(self,instr_logs):
        if instr_logs:
            for log in instr_logs:
                if isinstance(log,ins_log):
                    try:
                        InsConnector.SendLog(log)
                    except Exception as ex:
                        print ex  
                        
                        
    def send_instrument_status(self,instr_status):
        if instr_status:
            for item in instr_status:
                if isinstance(item,ins_status):
                    try:
                        InsConnector.SendStatus(item)
                    except Exception as ex:
                        print ex                                        

def test():
    from DBInterface.SqliteInterface import SqliteInterface

    with SqliteInterface() as db_interface:
        print 'getting reagent start...'
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
        except Exception as ex:
            print ex

if __name__ == '__main__':
    test()


