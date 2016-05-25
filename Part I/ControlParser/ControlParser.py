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

    parsing_mode = {'OFF':0,'SECTION':1,'ISE':2,'NORMAL':3}
    ise_test_start_flag = r'Test Name      Conc.  Unit        Mark            SAMPLE    BUFFER  Electrode/Refrence Lot  UserCode'
    normal_test_start_flag = r'Test Name      Conc.  Unit        Mark            ABS-RB       ABS  R1 LOT#  R2 LOT#  UserCode'

    def __init__(self):
        self.qc_list = []

    def extract_qc_info(self,qc_file_path):
        lates_control_file = GetLatestFile.get_latest_file(qc_file_path,'REALTIME MONITOR','.TXT')

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

        parsing_mode = ControlParser.parsing_mode['OFF']
        qc_lot = ''
        date_time = ''
        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str) and '' <> line.strip():
                    info_list = line.split()
                    if 2 == len(info_list):
                        parsing_mode = ControlParser.parsing_mode['SECTION']
                    elif ControlParser.ise_test_start_flag == line.strip():
                        parsing_mode = ControlParser.parsing_mode['ISE']
                    elif ControlParser.normal_test_start_flag == line.strip():
                        parsing_mode = ControlParser.parsing_mode['NORMAL']
                    elif ControlParser.parsing_mode['SECTION'] == parsing_mode:
                        qc_lot = info_list[3]
                        date_time = ' '.join(str(item) for item in info_list[-4:])
                    elif ControlParser.parsing_mode['ISE'] == parsing_mode:
                        #print info_list
                        test = info_list[0]
                        value = info_list[1]
                        unit = ''
                        abs_rb = info_list[2]
                        abs = info_list[3]
                        self.qc_list.append(ControlInfo(qc_lot,date_time,test,value,unit,abs_rb,abs))
                    elif ControlParser.parsing_mode['NORMAL'] == parsing_mode:
                        #print info_list
                        test = info_list[0]
                        value = info_list[1]
                        unit = info_list[2]
                        abs_rb = info_list[-3]
                        abs = info_list[-2]
                        self.qc_list.append(ControlInfo(qc_lot,date_time,test,value,unit,abs_rb,abs))
                    else:
                        parsing_mode = ControlParser.parsing_mode['OFF']

    def __repr__(self):
        return 'control info list:\n'+\
            '\n'.join(str(item) for item in self.qc_list)

def test():
    qc_parser = ControlParser()
    qc_parser.extract_qc_info('.')
    print qc_parser

if __name__ == '__main__':
    test()