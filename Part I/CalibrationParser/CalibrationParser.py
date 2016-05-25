from GetLatestFile.GetLatestFile import GetLatestFile


class CalibrationInfo():
    """
    definition for calibration data.
    """
    def __init__(self,cal_lot,date_time,test,value,unit,abs_rb,abs):
        self.cal_lot = cal_lot
        self.date_time = date_time
        self.test = test
        self.value = value
        self.unit = unit
        self.abs_rb = abs_rb
        self.abs = abs

    def __repr__(self):
        return 'cal lot:' + str(self.cal_lot) + '\t' +\
                'date time:' + str(self.date_time) + '\t' +\
                'test:' + str(self.test) + '\t' +\
                'value:' + str(self.value) + '\t' +\
                'unit:' + str(self.unit) + '\t' +\
                'abs_rb' + str(self.abs_rb) + '\t' +\
                'abs:' + str(self.abs)

class CalibrationParser():
    """
    calibration data parser from printed file.
    """
    parsing_mode = {'OFF':0,'SECTION':1,'TEST':2}
    section_start_flag = r'BLANK'
    test_start_flag = r'Test Name      Conc.  Unit        Mark            ABS-RB       ABS  R1 LOT#  R2 LOT#'

    def __init__(self):
        self.cal_list = []

    def extract_cal_info(self,cal_path):
        lates_cal_file = GetLatestFile.get_latest_file(cal_path,'REALTIME MONITOR','.TXT')

        file_content_list = []
        if lates_cal_file:
            # read file content into list.
            try:
                cal_file_handler = open(lates_cal_file)
                file_content_list = cal_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                cal_file_handler.close()

        parsing_mode = CalibrationParser.parsing_mode['OFF']
        cal_lot = ''
        date_time = ''
        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str):
                    if CalibrationParser.section_start_flag == line.strip():
                        parsing_mode = CalibrationParser.parsing_mode['SECTION']
                    elif CalibrationParser.test_start_flag == line.strip():
                        parsing_mode = CalibrationParser.parsing_mode['TEST']
                    elif CalibrationParser.parsing_mode['SECTION'] == parsing_mode:
                        info_list = line.split()
                        cal_lot = info_list[0]
                        date_time = ' '.join(str(item) for item in info_list[-4:])
                    elif CalibrationParser.parsing_mode['TEST'] == parsing_mode:
                        info_list = line.split()
                        if len(info_list) >= 4:
                            #print info_list
                            test = info_list[0]
                            value = info_list[1]
                            abs_rb = info_list[-2]
                            abs = info_list[-1]
                            unit = ''
                            if len(info_list) > 4:
                                unit = info_list[2]
                            self.cal_list.append(CalibrationInfo(cal_lot,date_time,test,value,unit,abs_rb,abs))
                    else:
                        parsing_mode = CalibrationParser.parsing_mode['OFF']

    def __repr__(self):
        return 'calibration info list:\n' +\
                '\n'.join(str(item) for item in self.cal_list)

def test():
    cal_parser = CalibrationParser()
    cal_parser.extract_cal_info('.')
    print cal_parser

if __name__ == '__main__':
    test()