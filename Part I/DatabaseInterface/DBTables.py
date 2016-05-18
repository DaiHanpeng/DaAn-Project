
class Common():
    def __init__(self):
        self.ID = 0
        self.Sent = 0
        self.SentDate = ''

class ins_heart(Common):
    def __init__(self):
        Common.__init__(self)


class ins_log(Common):
    def __init__(self):
        Common.__init__(self)


class ins_adjustment_result(Common):
    def __init__(self):
        Common.__init__(self)


class ins_calibration_result(Common):
    def __init__(self):
        Common.__init__(self)


class ins_calibration_status(Common):
    def __init__(self):
        Common.__init__(self)


class ins_qc(Common):
    def __init__(self):
        Common.__init__(self)


class ins_reagent(Common):
    def __init__(self):
        Common.__init__(self)
        self.Barcode = ''
        self.ExpireDate = ''
        self.LotNo = ''
        self.Name = ''
        self.OpenDate = ''
        self.OpenValidDays = ''
        self.Position = ''
        self.Quantity = ''
        self.TestCode = ''
        self.TestEnglishName = ''
        self.TestName = ''
        self.Unit = ''
        self.UsageDate = ''
        self.UsageType = ''

class ins_reagent_info(Common):
    def __init__(self):
        Common.__init__(self)
        self.AuthorizeInfo = ''
        self.LotNo = ''
        self.Position = ''
        self.RemainderCount = ''
        self.RemainderValue = ''
        self.TestCode = ''
        self.TestName = ''
        self.Type = ''

class ins_reagent_status(Common):
    def __init__(self):
        Common.__init__(self)
        self.RunDate = ''

class ins_status(Common):
    def __init__(self):
        Common.__init__(self)


class ins_test(Common):
    def __init__(self,barcode,result_value,test_code):
        Common.__init__(self)
        self.Absorbance = ''
        self.Barcode = barcode
        self.ReagentLotNo = ''
        self.RefHigh = ''
        self.RefLow = ''
        self.ResultDate = ''
        self.ResultValue = result_value
        self.SeqNo = ''
        self.TestCode = test_code
        self.Unit = ''

class ins_worklist_request(Common):
    def __init__(self):
        Common.__init__(self)


class ins_worklist_response(Common):
    def __init__(self):
        Common.__init__(self)


class ins_yingyang_compare(Common):
    def __init__(self):
        Common.__init__(self)

if __name__ == '__main__':
    print 'just for testing!'

    heart = ins_heart()
    print heart.ID

    input("press any key to continue...")
