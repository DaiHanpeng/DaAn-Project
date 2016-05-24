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

class ins_heart(Common,InsHeart):
    def __init__(self):
        Common.__init__(self)
        InsHeart.__init__(self)


class ins_log(Common,InsLog):
    def __init__(self):
        Common.__init__(self)
        InsLog.__init__(self)


class ins_adjustment_result(Common,InsAdjustmentResult):
    def __init__(self):
        Common.__init__(self)
        InsAdjustmentResult.__init__(self)


class ins_calibration_result(Common,InsCalibrationResult):
    def __init__(self):
        Common.__init__(self)
        InsCalibrationResult.__init__(self)


class ins_calibration_status(Common,InsCalibrationStatus):
    def __init__(self):
        Common.__init__(self)
        InsCalibrationStatus.__init__(self)


class ins_qc(Common,InsQC):
    def __init__(self):
        Common.__init__(self)
        InsQC.__init__(self)


class ins_reagent(Common,InsReagent):
    def __init__(self):
        Common.__init__(self)
        InsReagent.__init__(self)


class ins_reagent_info(Common,InsReagentInfo):
    def __init__(self):
        Common.__init__(self)
        InsReagentInfo.__init__(self)


class ins_reagent_status(Common,InsReagentStatus):
    def __init__(self):
        Common.__init__(self)
        InsReagentStatus.__init__(self)


class ins_status(Common,InsStatus):
    def __init__(self):
        Common.__init__(self)
        InsStatus.__init__(self)


class ins_test(Common,InsTest):
    def __init__(self):
        Common.__init__(self)
        InsTest.__init__(self)


class ins_worklist_request(Common,InsWorkListRequest):
    def __init__(self):
        Common.__init__(self)
        InsWorkListRequest.__init__(self)


class ins_worklist_response(Common,InsWorkListResponse):
    def __init__(self):
        Common.__init__(self)
        InsWorkListResponse.__init__(self)


class ins_yingyang_compare(Common,InsYinYangCompare):
    def __init__(self):
        Common.__init__(self)
        InsYinYangCompare.__init__(self)


if __name__ == '__main__':
    heart = ins_heart()
    print heart.ID
    input("press any key to continue...")
