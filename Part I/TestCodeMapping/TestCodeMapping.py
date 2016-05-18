from GetLatestFile.GetLatestFile import GetLatestFile


class AdviaChemistryTestCodeDictionary():
    """
    the whole map list of Advia chemistry.
    """
    def __init__(self):
        self.test_code_dictionary = {}

    def update_test_code(self,test,code):
        self.test_code_dictionary[code] = test
        #self.test_code_dictionary = dict((k,self.test_code_dictionary[k]) for k in sorted(self.test_code_dictionary.keys()))

    def build_test_code_dictionary_from_file(self,path_to_app_log):
        lates_reagent_file = GetLatestFile.get_latest_file(path_to_app_log,'Reagent','.txt')

        if lates_reagent_file:
            file_content_list = []
            # read file content into list.
            try:
                reagent_file_handler = open(lates_reagent_file)
                file_content_list = reagent_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                reagent_file_handler.close()

            #update test codes.
            file_content_list.reverse() #latest contents in the first position
            test_code_match_start = False
            if file_content_list:
                for item in file_content_list:
                    if isinstance(item,str):
                        if not test_code_match_start:
                            if -1 <> item.find(r'LAS_Response() Header: ID(8)'):
                                test_code_match_start = True
                        else:
                            if -1 <> item.find('CreateTestMapData'):
                                break
                            else:
                                if -1 <> item.find('[') and -1 <> item.find(']'):
                                    s1 = item.split('[')
                                    code = s1[1].split(']')[0]
                                    test = s1[2].split(']')[0]
                                    self.update_test_code(code=code,test=test)

    def __repr__(self):
        return 'test code dictionary:\n' + \
            '\n'.join(('test:' + str(self.test_code_dictionary[item]) + '\t' + 'code:' + str(item)) \
                    for item in self.test_code_dictionary)

def test1():
    test_code_dic = AdviaChemistryTestCodeDictionary()
    test_code_dic.update_test_code('na',301)
    test_code_dic.update_test_code('k',302)
    test_code_dic.update_test_code('cl',303)
    test_code_dic.update_test_code('alb',301)
    print test_code_dic

def test2():
    test_code_dic = AdviaChemistryTestCodeDictionary()
    path_to_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\LOG\APP'
    test_code_dic.build_test_code_dictionary_from_file(path_to_log_folder)
    print test_code_dic
    print '/////'

if __name__ == '__main__':
    test2()
    #print ("insert into InsReagentInfo values ('','','',?,'',?,?,'','0','')",['value','key','key'])


