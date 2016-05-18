# -*- coding: utf-8 -*-
from GetLatestFile.GetLatestFile import GetLatestFile

#: Message start token.
ASTM_STX = b'\x02'
#: Message end token.
ASTM_ETX = b'\x03'
#: Message chunk end token.
ASTM_ETB = b'\x17'

class TestResultInfo():
    """
    test result per sample.
    """
    def __init__(self,sample_id):
        self.sample_id = sample_id
        self.result_map = {} #map of test and result.
        self.flag_map = {}#map of test and flags.

    def update_result_map(self,test_code,result_value):
        self.result_map[test_code] = result_value

    def update_flag_map(self,test_code,result_flag):
        self.flag_map[test_code] = result_flag

    def __repr__(self):
        return '\nsample id:' + str(self.sample_id) + '\n'+\
            '\n'.join('test code:'+str(k)+'\t'+'result:'+str(self.result_map[k]) for k in self.result_map.keys())

class LISLogParser():
    """
    parser for lis log.
    """
    TEST_CODE_LEN = 3
    METHOD_LEN = 1
    RESULT_FIELD_LEN = 8
    FLAG_LEN = 3
    def __init__(self):
        self.result_list = []

    def extract_result_info_from_lis_log(self,log_folder_path):
        lates_lis_file = GetLatestFile.get_latest_file(log_folder_path,'LIS','.txt')

        self.result_list = []
        file_content_list = []

        if lates_lis_file:
            # read file content into list.
            try:
                lis_file_handler = open(lates_lis_file,'rb')
                file_content_list = lis_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
                print 'exception:',e
            finally:
                lis_file_handler.close()

        result_line_list = []
        if file_content_list:
            for line in file_content_list:
                if isinstance(line,str):
                    if -1 <> line.find(r'R 0') and -1 <> line.find(ASTM_STX) and \
                        -1 <> line.find(r'N0') and \
                            (-1 <> line.find(ASTM_ETB) or -1 <> line.find(ASTM_ETX)):
                        line = line.replace(b'\x00','')
                        if -1 <> line.find(r'R 0'):
                            line = line.split(r'R 0')[1]
                            if -1 <> line.find(ASTM_ETB):
                                line = line.split(ASTM_ETB)[0]
                            else:
                                line = line.split(ASTM_ETX)[0]
                            result_line_list.append(line)
                            #print line

        for result in result_line_list:
            if isinstance(result,str):
                info_list = result.split()
                sample_id = result.split()[0].split('N0')[1]

                for item in info_list:
                    if (item.endswith('M') or item.endswith('D') or item.endswith('U')) and \
                                    len(item)>1 and item[-4:-1].isdigit():
                        first_code_index = result.find(item)+len(item)-(LISLogParser.TEST_CODE_LEN+LISLogParser.METHOD_LEN)
                        #print item
                        break
                #print result[first_code_index:]

                index = first_code_index
                sample_result_info = TestResultInfo(sample_id)
                while index + 15 < len(result):
                    code = result[index:index+3].strip()
                    result_value = result[index+4:index+4+8].strip()
                    result_flag = result[index+4+8:index+4+8+3].strip()
                    if code and result_value:
                        sample_result_info.update_result_map(code,result_value)
                    if code and result_flag:
                        sample_result_info.update_flag_map(code,result_flag)
                    index += 15

                self.result_list.append(sample_result_info)

    def __repr__(self):
        return 'result list:\n' +\
            '\n'.join(repr(result) for result in self.result_list if isinstance(result,TestResultInfo))

def test():
    lis_log_parser = LISLogParser()
    lis_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\LOG\LIS'
    lis_log_parser.extract_result_info_from_lis_log(lis_log_folder)

    print lis_log_parser

if __name__ == '__main__':
    test()