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
    reagent_type_map = {'R1':0,'R2':1,'TOTAL':2}
    def __init__(self):
        self.date_time = ''
        self.system_id = ''
        self.reagent_info_list = []

    def update_reagent_info(self,reagent_name,type,count='',position='',cal_status=''):
        for item in self.reagent_info_list:
            if isinstance(item,PrintedReagentInfoItem):
                if item.reagent_name == reagent_name:
                    if self.reagent_type_map['R1'] == type:
                        item.r1_count = count
                        item.r1_position = position
                        item.r1_cal_status = cal_status
                    elif self.reagent_type_map['R2'] == type:
                        item.r2_count = count
                        item.r2_position = position
                        item.r2_cal_status = cal_status
                        #print item
                    elif self.reagent_type_map['TOTAL'] == type:
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

        if file_content_list:
            total_test_matching_flag = False
            for line in file_content_list:
                if isinstance(line,str):
                    if -1 <> line.find(r'Date/Time') and -1 <> line.find(r' : '):
                        self.date_time = line.split(r' : ')[1]
                    elif -1 <> line.find(r'System #') and -1 <> line.find(':'):
                        self.system_id = line.split(':')[1]
                    elif -1 <> line.find('R1'):
                        info_list = line.split()
                        if 8 == len(info_list):
                            reagent_name = info_list[0].strip()
                            position = info_list[2]
                            count = info_list[4]
                            cal_status = info_list[6]
                        elif 6 == len(info_list):
                            reagent_name = info_list[0].strip()
                            position = info_list[2]
                            count = info_list[3]
                            cal_status = ''
                        else:
                            reagent_name = line.split('R1')[0].strip()
                            info_list = line.split('R1')[1].split()
                            position = info_list[0]
                            count = info_list[2]
                            cal_status = info_list[5]
                        self.update_reagent_info(reagent_name,self.reagent_type_map['R1'],count,position,cal_status)
                    elif -1 <> line.find('R2'):
                        info_list = line.split('R2')
                        reagent_name = info_list[0].replace('*','')
                        reagent_name = reagent_name.replace('+','').strip()
                        info_list = info_list[1].split()
                        position = info_list[0]
                        if -1 <> line.find('+'):
                            count = info_list[3]
                        else:
                            count = info_list[2]
                        if len(info_list) >= 6:
                            cal_status = info_list[-2]
                        else:
                            cal_status = ''
                        self.update_reagent_info(reagent_name,self.reagent_type_map['R2'],count,position,cal_status)
                    elif -1 <> line.find(r'Test Name          Total # Tests'):
                        total_test_matching_flag = True
                    elif total_test_matching_flag:
                        info_list = line.split()
                        if len(info_list) >= 2:
                            reagent_name = ' '.join(str(item) for item in info_list[0:-1]).strip()
                            count = info_list[-1]
                            self.update_reagent_info(reagent_name,self.reagent_type_map['TOTAL'],count)

    def __repr__(self):
        return 'date time:' + str(self.date_time)+'\t'\
            'system id:' + str(self.system_id)+'\n'\
            ''.join(str(item) for item in self.reagent_info_list if isinstance(item,PrintedReagentInfoItem))

def test():
    reagent_parser = PrintedReagentInfoParser()
    file_path = r'..\Advia2400_ScreenCapture'
    reagent_parser.extract_info_from_printed_file(file_path)
    print reagent_parser

if __name__ == '__main__':
    test()