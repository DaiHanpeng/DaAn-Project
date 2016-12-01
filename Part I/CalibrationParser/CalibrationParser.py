import datetime
from GetLatestFile.GetLatestFile import GetLatestFile

from DatabaseInterface.MySqlTimestampInterface import MYSQL_DB_SCHEMA,TableTimestampInterface

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
                'abs_rb:' + str(self.abs_rb) + '\t' +\
                'abs:' + str(self.abs)

class CalibrationParser():
    MODULE_NAME = r'Calibration'
    """
    calibration data parser from printed file.
    """
    SECTION_LINE_MIN_LENGTH = 110
    RESULT_LINE_LENGTH = 91

    parsing_mode = {'OFF':0,'SECTION':1,'HEAD':2,'RESULT':3}
    section_start_flag = r'BLANK'
    HEAD_LINE = r'Test Name      Conc.  Unit        Mark            ABS-RB       ABS  R1 LOT#  R2 LOT#'

    def __init__(self):
        self.cal_list = []
        try:
            db_interface = TableTimestampInterface()
            db_interface.db_connect_initialize(MYSQL_DB_SCHEMA)
            self.last_updated_timestamp = db_interface.get_table_last_updated_timestamp(self.MODULE_NAME)
            print self.MODULE_NAME,' last updated timestamp: ', self.last_updated_timestamp
        except Exception as e:
            print 'db timestamp initialize failed!', e
        finally:
            db_interface.db_disconnect()

    def extract_cal_info(self,cal_path):
        self.cal_list = []
        last_updated_timestamp = self.last_updated_timestamp
        
        lates_cal_file = GetLatestFile.get_latest_file(cal_path,'Calibration_','.TXT')

        print lates_cal_file

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

        #1, matching a section
        #2, matching a head
        #3, matching calibration results...
        #4, matching an empty line
        # ,matching next section...
        parsing_mode = CalibrationParser.parsing_mode['SECTION']
        cal_lot = ''
        date_time = ''

        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str) and len(line.strip()) > 0:
                    #SECTION mode
                    if CalibrationParser.parsing_mode['SECTION'] == parsing_mode:
                        #SECTION matched, turn to HEAD.
                        if CalibrationParser.SECTION_LINE_MIN_LENGTH < len(line.strip()):
                            parsing_mode = CalibrationParser.parsing_mode['HEAD']
                            #
                            cal_lot = line[0:14]
                            date_time = line[98:].strip()
                            #print cal_lot, date_time
                    #HEAD mode
                    elif CalibrationParser.parsing_mode['HEAD'] == parsing_mode:
                        # HEAD matched, turn to calibration results.
                        if CalibrationParser.HEAD_LINE == line.strip():
                            parsing_mode = CalibrationParser.parsing_mode['RESULT']
                    #RESULT mode
                    elif CalibrationParser.parsing_mode['RESULT'] == parsing_mode:
                        #
                        if CalibrationParser.RESULT_LINE_LENGTH == len(line):
                            test = line[0:10].strip()
                            value = line[10:22].strip()
                            unit = line[22:30].strip()
                            abs_rb = line[46:58].strip()
                            abs = line[58:68].strip()

                            if cal_lot and date_time:
                                f_date_time = datetime.datetime.strptime(date_time,'%d %b %Y %H:%M:%S')
                                if f_date_time > last_updated_timestamp:
                                    cal_info = CalibrationInfo(cal_lot,f_date_time,test,value,unit,abs_rb,abs)
                                    self.cal_list.append(cal_info)
                                    if f_date_time > self.last_updated_timestamp:
                                        self.last_updated_timestamp = f_date_time
                else:
                    #empty line, must match next SECTION.
                    cal_lot = ''
                    date_time = ''
                    parsing_mode = CalibrationParser.parsing_mode['SECTION']

        if self.last_updated_timestamp > last_updated_timestamp:
            try:
                db_interface = TableTimestampInterface()
                db_interface.db_connect_initialize(MYSQL_DB_SCHEMA)
                db_interface.update_table_timestamp(self.MODULE_NAME,self.last_updated_timestamp)
            except Exception as e:
                print 'db update timestamp failed!', e
            finally:
                db_interface.db_disconnect()


    def __repr__(self):
        return 'calibration info list:\n' +\
                '\n'.join(str(item) for item in self.cal_list)

def test():
    cal_parser = CalibrationParser()
    #cal_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\Reports\Training_Center_2400_Reports\Reports'
    cal_path = '.'
    cal_parser.extract_cal_info(cal_path)
    print cal_parser

if __name__ == '__main__':
    test()