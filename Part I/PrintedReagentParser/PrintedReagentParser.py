from GetLatestFile.GetLatestFile import GetLatestFile

class PrintedReagentInfoItem():
    """
    the definition of reagent information from printed file.
    """
    def __init__(self,reagent_name):
        self.reagent_name = reagent_name
        self.r1_count = ''
        self.r1_position = ''
        self.r1_cal_status = ''
        self.r2_count = ''
        self.r2_position = ''
        self.total_count = ''
        self.r2_cal_status = ''

    def __repr__(self):
        return ''.join('reagent:'+str(self.reagent_name)+'\t'\
                        'r1:'+str(self.r1_count)+'\t'\
                        'r1 position:'+str(self.r1_position)+'\t'\
                        'r1 cal status:'+str(self.r1_cal_status)+'\t'\
                        'r2:'+str(self.r2_count)+'\t'\
                        'r2 position:'+str(self.r2_position)+'\t'\
                        'r2 cal status:'+str(self.r2_cal_status)+'\t'\
                        'total:'+str(self.total_count))


class PrintedReagentInfoParser():
    """
    reagent info parser for printed file.
    """
    reagent_type_map = {'OFF':0,'R1_HEAD':1,'R1_REAGENT':2,'R2_HEAD':3,'R2_REAGENT':4,'TOTAL_HEAD':5,'TOTAL_REAGENT':6}

    #R1_HEAD_LINE = r'***** Reagent Inventory Summary for <RTT1> *****'
    #R2_HEAD_LINE = r'***** Reagent Inventory Summary for <RTT2> *****'
    R1_R2_HEAD_LINE = r'Deselect  Test Name         R  Posi.#   Backup   #Tests    Lot#   Exp.Date         Cal Interval  CalStatus                          QCStatus         Remaining'

    TOTAL_HEAD_LINE = r'***** Total Tests Summary Table *****'
    TOTAL_LINE = r'Test Name          Total # Tests'


    def __init__(self):
        self.date_time = ''
        self.system_id = ''
        self.reagent_info_list = []

    def update_reagent_info(self,reagent_name,type,count='',position='',cal_status=''):
        for item in self.reagent_info_list:
            if isinstance(item,PrintedReagentInfoItem):
                if item.reagent_name == reagent_name:
                    if self.reagent_type_map['R1_REAGENT'] == type:
                        item.r1_count = count
                        item.r1_position = position
                        item.r1_cal_status = cal_status
                    elif self.reagent_type_map['R2_REAGENT'] == type:
                        item.r2_count = count
                        item.r2_position = position
                        item.r2_cal_status = cal_status
                        #print item
                    elif self.reagent_type_map['TOTAL_REAGENT'] == type:
                        item.total_count = count
                    return
        self.reagent_info_list.append(PrintedReagentInfoItem(reagent_name))
        self.update_reagent_info(reagent_name,type,count,position,cal_status)

    def extract_info_from_printed_file(self,file_path):
        self.reagent_info_list = []
        lates_printed_file = GetLatestFile.get_latest_file(file_path,'REAGENT','.TXT')

        file_content_list = []
        if lates_printed_file:
            # read file content into list.
            try:
                printed_file_handler = open(lates_printed_file)
                file_content_list = printed_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                printed_file_handler.close()

        #R1 Head
        parsing_mode = PrintedReagentInfoParser.reagent_type_map['R1_HEAD']

        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str) and len(line.strip()) > 0:
                    if PrintedReagentInfoParser.reagent_type_map['R1_HEAD'] == parsing_mode:
                        # update date time and system id.
                        if line.find(r'Date/Time :') <> -1:
                            self.date_time = line[11:].strip()
                        elif line.find(r'System # :') <> -1:
                            self.system_id = line[10:].strip()
                        #
                        if PrintedReagentInfoParser.R1_R2_HEAD_LINE == line.strip():
                            parsing_mode = PrintedReagentInfoParser.reagent_type_map['R1_REAGENT']
                    elif PrintedReagentInfoParser.reagent_type_map['R1_REAGENT'] == parsing_mode:
                        #R1 reagent item processing
                        if r'R1' == line[28:30]:
                            reagent_name = line[10:24].strip()
                            count = line[50:56].strip()
                            position = line[32:37].strip()
                            cal_status = line[99:105].strip()
                            self.update_reagent_info(reagent_name,self.reagent_type_map['R1_REAGENT'],count,position,cal_status)
                    elif PrintedReagentInfoParser.reagent_type_map['R2_HEAD'] == parsing_mode:
                        if PrintedReagentInfoParser.R1_R2_HEAD_LINE == line.strip():
                            parsing_mode = PrintedReagentInfoParser.reagent_type_map['R2_REAGENT']
                    elif PrintedReagentInfoParser.reagent_type_map['R2_REAGENT'] == parsing_mode:
                        # R2 Reagent item processing
                        if r'R2' == line[28:30]:
                            reagent_name = line[10:24].strip()
                            count = line[50:56].strip()
                            position = line[32:37].strip()
                            cal_status = line[99:105].strip()
                            self.update_reagent_info(reagent_name,self.reagent_type_map['R2_REAGENT'],count,position,cal_status)
                    elif PrintedReagentInfoParser.reagent_type_map['TOTAL_HEAD'] == parsing_mode:
                        if PrintedReagentInfoParser.TOTAL_LINE == line.strip():
                            parsing_mode = PrintedReagentInfoParser.reagent_type_map['TOTAL_REAGENT']
                    elif PrintedReagentInfoParser.reagent_type_map['TOTAL_REAGENT'] == parsing_mode:
                        #total reagent info processing
                        reagent_name = line[2:20].strip()
                        count = line[25:].strip()
                        self.update_reagent_info(reagent_name,self.reagent_type_map['TOTAL_REAGENT'],count)
                else:
                    if PrintedReagentInfoParser.reagent_type_map['R1_REAGENT'] == parsing_mode:
                        parsing_mode = PrintedReagentInfoParser.reagent_type_map['R2_HEAD']
                    elif PrintedReagentInfoParser.reagent_type_map['R2_REAGENT'] == parsing_mode:
                        parsing_mode = PrintedReagentInfoParser.reagent_type_map['TOTAL_HEAD']

    def __repr__(self):
        return 'date time:' + str(self.date_time)+'\t' \
            'system id:' + str(self.system_id) + '\n' +\
            '\n'.join(str(item) for item in self.reagent_info_list if isinstance(item,PrintedReagentInfoItem))

def test():
    reagent_parser = PrintedReagentInfoParser()
    file_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\Reports\DaAn_Reports\Reports'
    reagent_parser.extract_info_from_printed_file(file_path)
    print reagent_parser

if __name__ == '__main__':
    test()