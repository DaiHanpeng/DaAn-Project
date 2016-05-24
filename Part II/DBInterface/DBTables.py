import clr
from System import *

clr.AddReferenceToFileAndPath('Daan.Instrument.Connector.dll')

from Daan.Instrument.Entity import *
from Daan.Instrument.Type import *

class Common():
    def __init__(self):
        self.ID = 0
        self.Sent = 0
        self.SentDate = ''

    def __repr__(self):
        return 'ID:'+str(self.ID)+'\t'+\
            'Sent:'+str(self.Sent)+'\t'+\
            'SentDate:'+str(self.SentDate)


class ins_heart(Common,InsHeart):
    def __init__(self):
        Common.__init__(self)
        InsHeart.__init__(self)

    def __repr__(self):
        return 'RunDate:'+str(self.RunDate)+'\t'+\
                'TempReagent:'+str(self.TempReagent)+'\t'+\
                'TempIncubation:'+str(self.TempIncubation)+'\t'+\
                'CleaningFluid:'+str(self.CleaningFluid)+'\t'+\
                'Detergent:'+str(self.Detergent)+'\t'+\
                'Effluent:'+str(self.Effluent)+'\t'+\
                'Temperature:'+str(self.Temperature)+'\t'+\
                'SubstrateA:'+str(self.SubstrateA)+'\t'+\
                'SubstrateB:'+str(self.SubstrateB)+'\t'+\
                'PositivePressure:'+str(self.PositivePressure)+'\t'+\
                'NegativePressure:'+str(self.NegativePressure)+'\t'+\
                super(ins_heart, self).__repr__()


class ins_log(Common,InsLog):
    def __init__(self):
        Common.__init__(self)
        InsLog.__init__(self)

    def __repr__(self):
        return 'Content:'+str(self.Content)+'\t'+\
            'LogType:'+str(self.LogType)+'\t'+\
            'RunDate'+str(self.RunDate)+'\t'+\
            'Status:'+str(self.Status)+'\t'+\
            super(ins_log, self).__repr__()


class ins_adjustment_result(Common,InsAdjustmentResult):
    def __init__(self):
        Common.__init__(self)
        InsAdjustmentResult.__init__(self)

    def __repr__(self):
        return 'not implemented yet...'


class ins_calibration_result(Common,InsCalibrationResult):
    def __init__(self):
        Common.__init__(self)
        InsCalibrationResult.__init__(self)

    def __repr__(self):
        return 'Absorbance:'+str(self.Absorbance)+'\t'+\
                'Barcode:'+str(self.Barcode)+'\t'+\
                'ExpireDate:'+str(self.ExpireDate)+'\t'+\
                'LotNo:'+str(self.LotNo)+'\t'+\
                'Name:'+str(self.Name)+'\t'+\
                'OpenDate:'+str(self.OpenDate)+'\t'+\
                'OpenValidDays:'+str(self.OpenValidDays)+'\t'+\
                'ReagentLotNo:'+str(self.ReagentLotNo)+'\t'+\
                'ResultDate:'+str(self.ResultDate)+'\t'+\
                'ResultValue:'+str(self.ResultValue)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'Type:'+str(self.Type)+'\t'+\
                'Unit:'+str(self.Unit)+'\t'+\
                super(ins_calibration_result, self).__repr__()


class ins_calibration_status(Common,InsCalibrationStatus):
    def __init__(self):
        Common.__init__(self)
        InsCalibrationStatus.__init__(self)

    def __repr__(self):
        return 'calibrationResults:'+str(self.calibrationResults)+'\t'+\
                'Curve:'+str(self.Curve)+'\t'+\
                'FitRate:'+str(self.FitRate)+'\t'+\
                'LotNo:'+str(self.LotNo)+'\t'+\
                'ReagentLotNo:'+str(self.ReagentLotNo)+'\t'+\
                'ResultDate:'+str(self.ResultDate)+'\t'+\
                'State:'+str(self.State)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'TtlNums:'+str(self.TtlNums)+'\t'+\
                super(ins_calibration_status, self).__repr__()


class ins_qc(Common,InsQC):
    def __init__(self):
        Common.__init__(self)
        InsQC.__init__(self)

    def __repr__(self):
        return 'Absorbance:'+str(self.Absorbance)+'\t'+\
                'Barcode:'+str(self.Barcode)+'\t'+\
                'ExpireDate:'+str(self.ExpireDate)+'\t'+\
                'LotNo:'+str(self.LotNo)+'\t'+\
                'Name:'+str(self.Name)+'\t'+\
                'OneSD:'+str(self.OneSD)+'\t'+\
                'OpenDate:'+str(self.OpenDate)+'\t'+\
                'OpenValidDays:'+str(self.OpenValidDays)+'\t'+\
                'ReagentLotNo:'+str(self.ReagentLotNo)+'\t'+\
                'ResultDate:'+str(self.ResultDate)+'\t'+\
                'ResultValue:'+str(self.ResultValue)+'\t'+\
                'TargetValue:'+str(self.TargetValue)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'Type:'+str(self.Type)+'\t'+\
                'Unit:'+str(self.Unit)+'\t'+\
                super(ins_qc, self).__repr__()


class ins_reagent(Common,InsReagent):
    def __init__(self):
        Common.__init__(self)
        InsReagent.__init__(self)

    def __repr__(self):
        return 'Barcode:'+str(self.Barcode)+'\t'+\
                'ExpireDate:'+str(self.ExpireDate)+'\t'+\
                'LotNo:'+str(self.LotNo)+'\t'+\
                'Name:'+str(self.Name)+'\t'+\
                'OpenDate:'+str(self.OpenDate)+'\t'+\
                'OpenValidDays:'+str(self.OpenValidDays)+'\t'+\
                'Position:'+str(self.Position)+'\t'+\
                'Quantity:'+str(self.Quantity)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'TestEnglishName:'+str(self.TestEnglishName)+'\t'+\
                'TestName:'+str(self.TestName)+'\t'+\
                'Unit:'+str(self.Unit)+'\t'+\
                'UsageDate:'+str(self.UsageDate)+'\t'+\
                'UsageType:'+str(self.UsageType)+'\t'+\
                super(ins_reagent, self).__repr__()


class ins_reagent_info(Common,InsReagentInfo):
    def __init__(self):
        Common.__init__(self)
        InsReagentInfo.__init__(self)

    def __repr__(self):
        return 'AuthorizeCount:'+str(self.AuthorizeCount)+'\t'+\
                'LotNo:'+str(self.LotNo)+'\t'+\
                'Position:'+str(self.Position)+'\t'+\
                'RemainderCount:'+str(self.RemainderCount)+'\t'+\
                'RemainderValue:'+str(self.RemainderValue)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'TestName:'+str(self.TestName)+'\t'+\
                'Type:'+str(self.Type)+'\t'+\
                super(ins_reagent_info, self).__repr__()

class ins_reagent_status(Common,InsReagentStatus):
    def __init__(self):
        Common.__init__(self)
        InsReagentStatus.__init__(self)

    def __repr__(self):
        return 'not implemented yet...'

class ins_status(Common,InsStatus):
    def __init__(self):
        Common.__init__(self)
        InsStatus.__init__(self)

    def __repr__(self):
        return 'RunDate:'+str(self.RunDate)+'\t'+\
                'StatusCode:'+str(self.StatusCode)+'\t'+\
                super(ins_status, self).__repr__()

class ins_test(Common,InsTest):
    def __init__(self):
        Common.__init__(self)
        InsTest.__init__(self)

    def __repr__(self):
        return 'Absorbance:'+str(self.Absorbance)+'\t'+\
                'Barcode:'+str(self.Barcode)+'\t'+\
                'ReagentLotNo:'+str(self.ReagentLotNo)+'\t'+\
                'RefHigh:'+str(self.RefHigh)+'\t'+\
                'RefLow:'+str(self.RefLow)+'\t'+\
                'ResultDate:'+str(self.ResultDate)+'\t'+\
                'ResultValue:'+str(self.ResultValue)+'\t'+\
                'SeqNo:'+str(self.SeqNo)+'\t'+\
                'TestCode:'+str(self.TestCode)+'\t'+\
                'Unit:'+str(self.Unit)+'\t'+\
                super(ins_test, self).__repr__()


class ins_worklist_request(Common,InsWorkListRequest):
    def __init__(self):
        Common.__init__(self)
        InsWorkListRequest.__init__(self)

    def __repr__(self):
        return 'not implemented yet...'


class ins_worklist_response(Common,InsWorkListResponse):
    def __init__(self):
        Common.__init__(self)
        InsWorkListResponse.__init__(self)

    def __repr__(self):
        return 'not implemented yet...'


class ins_yingyang_compare(Common,InsYinYangCompare):
    def __init__(self):
        Common.__init__(self)
        InsYinYangCompare.__init__(self)

    def __repr__(self):
        return 'not implemented yet...'        

if __name__ == '__main__':
    heart = ins_heart()
    print heart.ID
    input("press any key to continue...")
