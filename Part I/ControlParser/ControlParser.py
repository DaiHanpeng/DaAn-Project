from GetLatestFile.GetLatestFile import GetLatestFile

class ControlInfo():
    """
    definition for control data.
    """
    def __init__(self,qc_lot,date_time,test,value,unit,abs_rb,abs):
        self.qc_lot = qc_lot
        self.date_time = date_time
        self.test = test
        self.value = value
        self.unit = unit
        self.abs_rb = abs_rb
        self.abs = abs

    def __repr__(self):
        return 'lot:' + str(self.qc_lot) + '\t'+\
                'date time:' + str(self.date_time) + '\t' +\
                'test:' + str(self.test) + '\t' +\
                'value:' + str(self.value) + '\t' +\
                'unit:' + str(self.unit) + '\t' +\
                'abs-rb:' + str(self.abs_rb) + '\t' +\
                'abs:' + str(self.abs)

class ControlParser():
    """
    parser for control data from printed file.
    """

    parsing_mode = {'OFF':0,'SECTION':1,'HEAD':2,'REAULT':3}

    SECTION_LINE_MIN_LENGTH = 110
    ISE_HEAD_LINE = r'Test Name      Conc.  Unit        Mark            SAMPLE    BUFFER  Electrode/Refrence Lot  UserCode'
    NORMAL_HEAD_LINE = r'Test Name      Conc.  Unit        Mark            ABS-RB       ABS  R1 LOT#  R2 LOT#  UserCode'


    def __init__(self):
        self.qc_list = []

    def extract_qc_info(self,qc_file_path):
        lates_control_file = GetLatestFile.get_latest_file(qc_file_path,'Control_','.TXT')

        file_content_list = []
        if lates_control_file:
            # read file content into list.
            try:
                control_file_handler = open(lates_control_file)
                file_content_list = control_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                control_file_handler.close()

        parsing_mode = ControlParser.parsing_mode['SECTION']
        qc_lot = ''
        date_time = ''
        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str) and len(line.strip()) > 0:
                    # SECTION mode
                    if ControlParser.parsing_mode['SECTION'] == parsing_mode:
                        if ControlParser.SECTION_LINE_MIN_LENGTH < len(line.strip()):
                            parsing_mode = ControlParser.parsing_mode['HEAD']

                            qc_lot = line[22:32].strip()
                            date_time = line[98:].strip()
                    # HEAD mode
                    elif ControlParser.parsing_mode['HEAD'] == parsing_mode:
                        if ControlParser.ISE_HEAD_LINE == line.strip() or\
                            ControlParser.NORMAL_HEAD_LINE == line.strip():
                            parsing_mode = ControlParser.parsing_mode['REAULT']
                    #RESULT mode
                    elif ControlParser.parsing_mode['REAULT'] == parsing_mode:
                        if qc_lot and date_time:
                            test = line[0:10].strip()
                            value = line[12:21].strip()
                            unit = line[22:33].strip()
                            abs_rb = line[46:57].strip()
                            abs = line[58:67].strip()

                            qc_info = ControlInfo(qc_lot,date_time,test,value,unit,abs_rb,abs)
                            self.qc_list.append(qc_info)
                else:
                    qc_lot = ''
                    date_time = ''
                    parsing_mode = ControlParser.parsing_mode['SECTION']

    def __repr__(self):
        return 'control info list:\n'+\
            '\n'.join(str(item) for item in self.qc_list)

def test():
    qc_parser = ControlParser()
    qc_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\Reports\DaAn_Reports\Reports'
    qc_parser.extract_qc_info(qc_path)
    print qc_parser

if __name__ == '__main__':
    test()