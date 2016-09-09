from GetLatestFile.GetLatestFile import GetLatestFile
import os
import time

class InstrumentLogInfo():
    """
    definition of instrument log info.
    """
    LOG_TYPE = {"NORMAL":1,"WARMING":2,"EXCEPTION":3}

    def __init__(self,date_time,log_type,log_content):
        self.date_time = date_time
        self.log_type = log_type
        self.log_content = log_content

    def __repr__(self):
        return 'date time:' + str(self.date_time) + '\t' +\
        'log type:' + str(self.log_type) + '\t' +\
        'log content:' + str(self.log_content)


class InstrumentStatusInfo():
    """
    definition of instrument status info
    """
    STATUS_TYPE = {"START":0,"PAUSE":1,"STOP":2,"FINISHED":3,"POWER_ON":4,"POWER_OFF":5}

    def __init__(self,date_time,status_type):
        self.date_time = date_time
        self.status_type = status_type

    def __repr__(self):
        return 'date time:' + str(self.date_time) + '\t' +\
        'status type:' + str(self.status_type)


class ErrorReportParser():
    """
    parser for printed error file.
    extracting info of instrument log instrument status.
    """
    PARSING_MODE = {"LOG_HEAD":1,"LOG_ITEM":2}

    LOG_HEAD = r'No.    Date    Section     Mode           Samp.ID     Test     Safe.No.    Contents                            Measures'

    INSTRUMENT_START = r"INITIALIZE"
    INSTRUMENT_PAUSE = r"PAUSE" #contianing this word
    INSTRUMENT_STOP = r"END"
    INSTRUMENT_FINISHED = r"READY"
    #INSTRUMENT_POWER_ON = r""
    #INSTRUMENT_POWER_OFF = r""


    def __init__(self):
        self.instrment_status = InstrumentStatusInfo(date_time='',status_type=InstrumentStatusInfo.STATUS_TYPE["POWER_OFF"])
        self.instrment_log_list = []
        self.first_launch_flag = True
        self.last_update_date_time = r''

    def extract_error_report_info(self,error_report_path):
        lates_err_report_file = GetLatestFile.get_latest_file(error_report_path,'Error_','.TXT')


        file_content_list = []
        self.instrment_log_list = []

        if lates_err_report_file:
            # read file content into list.
            try:
                control_file_handler = open(lates_err_report_file)
                file_content_list = control_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                control_file_handler.close()

        parsing_mode = ErrorReportParser.PARSING_MODE["LOG_HEAD"]
        instrument_status_parsered = False

        latest_update_date_time = self.last_update_date_time

        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str) and len(line.strip()) > 0:
                    if ErrorReportParser.PARSING_MODE["LOG_HEAD"] == parsing_mode:
                        #head matched, turn to item mode.
                        if ErrorReportParser.LOG_HEAD == line.strip():
                            parsing_mode = ErrorReportParser.PARSING_MODE["LOG_ITEM"]
                    elif ErrorReportParser.PARSING_MODE["LOG_ITEM"] == parsing_mode:
                        date_time = line[5:18].strip()

                        year = time.strftime("%Y",time.localtime(time.time()))
                        month = date_time[:2]
                        day = date_time[3:5]
                        hour = date_time[6:8]
                        minute = date_time[9:]

                        #"2006-1-16 2:28:22"
                        date_time = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+'00'

                        #update the latest log time stamp.
                        if latest_update_date_time < date_time:
                            latest_update_date_time = date_time

                        #only new record should be updated.
                        if self.last_update_date_time >= date_time:

                            print 'parser breaked!!!'
                            break;#return from the for loop...

                        log_content = line[68:110].strip()
                        str_log_type = line[111:].strip()
                        if r"WARNING" == str_log_type:
                            log_type = InstrumentLogInfo.LOG_TYPE["WARMING"]
                        elif r"STOP" == str_log_type:
                            log_type = InstrumentLogInfo.LOG_TYPE["EXCEPTION"]
                        else:
                            log_type = InstrumentLogInfo.LOG_TYPE["NORMAL"]

                        #make instrument log items
                        log_item = InstrumentLogInfo(date_time,log_type,log_content)
                        self.instrment_log_list.append(log_item)

                        #parsing for instrument status update.
                        if not instrument_status_parsered:
                            instrument_status_parsered = True
                            instrument_status = line[24:39].strip()
                            status_type = InstrumentStatusInfo.STATUS_TYPE["FINISHED"]
                            if ErrorReportParser.INSTRUMENT_START == instrument_status:
                                status_type = InstrumentStatusInfo.STATUS_TYPE["START"]
                            elif instrument_status.find(ErrorReportParser.INSTRUMENT_PAUSE) <> -1:
                                status_type = InstrumentStatusInfo.STATUS_TYPE["PAUSE"]
                            elif ErrorReportParser.INSTRUMENT_STOP == instrument_status:
                                status_type = InstrumentStatusInfo.STATUS_TYPE["STOP"]
                            elif ErrorReportParser.INSTRUMENT_FINISHED == instrument_status:
                                status_type = InstrumentStatusInfo.STATUS_TYPE["FINISHED"]

                            #update instrument status if status changed.
                            self.instrment_status.status_type = status_type
                            self.instrment_status.date_time = date_time

    def __repr__(self):
        return 'instrument info list:\n'+\
            '\n'.join(str(item) for item in self.instrment_log_list) + \
               '\n instrument status:\n' + repr(self.instrment_status)

def test():
    err_report_parser = ErrorReportParser()
    err_report_path = r'.'
    err_report_parser.extract_error_report_info(err_report_path)
    print err_report_parser

if __name__ == '__main__':
    test()
    #print "08/02 14:23" < "08/02 13:25"

















