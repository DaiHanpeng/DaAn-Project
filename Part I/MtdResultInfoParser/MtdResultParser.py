from GetLatestFile.GetLatestFile import GetLatestFile
import datetime


class ResultInfo():
    """
    definition of single one test result item.
    """
    def __init__(self,sample_id,date_time,test_name,value,unit='',abs_rb='',abs=''):
        self.sample_id = sample_id
        self.date_time = date_time
        self.test_name = test_name
        self.value = value
        self.unit = unit
        self.abs_rb = abs_rb
        self.abs = abs

    def __repr__(self):
        return 'sample id:' + str(self.sample_id) + '\t' +\
                'date time:' + str(self.date_time) + '\t' +\
                'test name:' + str(self.test_name) + '\t' +\
                'value:' + str(self.value) + '\t' +\
                'unit:' + str(self.unit) + '\t' +\
                'abs_rb:' + str(self.abs_rb) + '\t' +\
                'abs:' + str(self.abs)

class MtdResultParser():
    """
    parser for test result information from .mtd file.
    """
    result_type_map = {'OFF':0,'START':1,'ISE':2,'HIL':3,'NORMAL':4,'CALCULTED':5}

    def __init__(self):
        self.result_list = []
        self.last_time_stamp = None

    def build_result_info_from_mtd_file(self,mtd_folder_path):
        lates_mtd_file = GetLatestFile.get_latest_file(mtd_folder_path,'','.MTD')

        self.result_list = []
        file_content_list = []
        if lates_mtd_file:
            # read file content into list.
            try:
                mtd_file_handler = open(lates_mtd_file)
                file_content_list = mtd_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                mtd_file_handler.close()

        if file_content_list:
            matching_status = self.result_type_map['OFF']
            for line in file_content_list:
                if isinstance(line,str):
                    #start of test result block.
                    #0103191635               CHEN HONG YOU             19500101     M  Year       66     Serum       1.0 4/28/2016 10:50:09
                    ISE_RESULT_HEADER = 'Test Name      Conc.  Unit        Mark            SAMPLE    BUFFER  Electrode/Refrence Lot  UserCode'
                    HIL_RESULT_HEADER = 'Test Name      Conc.  Mark          UserCode    ABS-RB       ABS  Measurement test name'
                    NORMAL_RESULT_HEADER = 'Test Name      Conc.  Unit        Mark            ABS-RB       ABS  R1 LOT#  R2 LOT#  UserCode'
                    CALCULATED_RESULT_HEADER = r'Test Name      Conc.  Unit        Mark          UserCode'
                    RESULT_FLAG = 'XYZ'
                    if -1 <> line.find('Year') and -1 <> line.find(':') and -1 <> line.find('/'):
                        splitted_line_list = line.split()
                        sample_id = splitted_line_list[0]
                        sample_date_time = splitted_line_list[-2] + ' ' + splitted_line_list[-1]
                        # Attention!
                        # the date time format may vary...
                        date_time = datetime.datetime.strptime(sample_date_time,'%m/%d/%Y %H:%M:%S')
                        if self.last_time_stamp:
                            if date_time > self.last_time_stamp:
                                matching_status = self.result_type_map['START']
                                self.last_time_stamp = date_time
                            else:
                                matching_status = self.result_type_map['OFF']
                        else:
                            matching_status = self.result_type_map['START']
                            self.last_time_stamp = date_time
                    elif -1 <> line.find(ISE_RESULT_HEADER):
                        if matching_status <> self.result_type_map['OFF']:
                            matching_status = self.result_type_map['ISE']
                    elif -1 <> line.find(HIL_RESULT_HEADER):
                        if matching_status <> self.result_type_map['OFF']:
                            matching_status = self.result_type_map['HIL']
                    elif -1 <> line.find(NORMAL_RESULT_HEADER):
                        if matching_status <> self.result_type_map['OFF']:
                            matching_status = self.result_type_map['NORMAL']
                    elif -1 <> line.find(CALCULATED_RESULT_HEADER):
                        if matching_status <> self.result_type_map['OFF']:
                            matching_status = self.result_type_map['CALCULTED']
                    elif -1 <> line.find(RESULT_FLAG):
                        splitted_line_list = line.split()
                        test_name = splitted_line_list[0]
                        value = splitted_line_list[1]
                        if self.result_type_map['ISE'] == matching_status:
                            self.result_list.append(ResultInfo(sample_id,str(date_time),test_name,value))
                        elif self.result_type_map['HIL'] == matching_status:
                            abs_rb = splitted_line_list[3]
                            abs = splitted_line_list[4]
                            self.result_list.append(ResultInfo(sample_id,str(date_time),test_name,value,'',abs_rb,abs))
                        elif self.result_type_map['NORMAL'] == matching_status:
                            unit = ''
                            if 'Saline' <> test_name:
                                unit = splitted_line_list[2]
                            abs_rb = splitted_line_list[-3]
                            abs = splitted_line_list[-2]
                            self.result_list.append(ResultInfo(sample_id,str(date_time),test_name,value,unit,abs_rb,abs))
                        elif self.result_type_map['CALCULTED'] == matching_status:
                            unit = r'%'
                            self.result_list.append(ResultInfo(sample_id,str(date_time),test_name,value,unit))
                        else:
                            matching_status = self.result_type_map['OFF']
                    else:
                        matching_status = self.result_type_map['OFF']

    def __repr__(self):
        return '\n'.join(repr(item) for item in self.result_list)


def test_result_info():
    print ResultInfo('12345','4/28/2016 08:00:31','Alb','12.3','g/L','0.123','0.234')

def test():
    mtd_folder = r'G:\05_DaAn\Mtd_Calculated_Result'
    mtd_parser = MtdResultParser()
    mtd_parser.build_result_info_from_mtd_file(mtd_folder)
    print mtd_parser

if __name__ == '__main__':
    #test_result_info()
    test()

'''
    import time,datetime

    str_time1 = '4/28/2016 08:00:31'
    str_time2 = '4/28/2016 08:01:31'

    DT1 = datetime.datetime.strptime(str_time1, "%m/%d/%Y %H:%M:%S")
    DT2 = datetime.datetime.strptime(str_time2, "%m/%d/%Y %H:%M:%S")
    print str(DT1)
    print str(DT2)
    print DT1 > DT2
'''
