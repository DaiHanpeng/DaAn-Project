from GetLatestFile.GetLatestFile import GetLatestFile

class ReagentDict():
    """
    Reagent list per analyzer.
    """
    def __init__(self):
        self.reagent_dict = dict()

    def update_reagent(self,reagent,count):
        self.reagent_dict[reagent] = count

    def build_test_code_dictionary_from_file(self,path_to_app_log):
        lates_reagent_file = GetLatestFile.get_latest_file(path_to_app_log,'Reagent','.txt')

        file_content_list = []
        if lates_reagent_file:
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
                                    #code = s1[1].split(']')[0]
                                    reagent = s1[2].split(']')[0]
                                    count = s1[2].split(']')[1].split(' ')[-1]
                                    self.update_reagent(reagent,count)

    def __repr__(self):
        return 'reagent list:\n' + ''.join(('test:' + str(k) +'\t' +'count:' + str(self.reagent_dict[k])) for k in self.reagent_dict.keys())

def test1():
    reagent_list = ReagentDict()
    reagent_list.update_reagent('Alb',100)
    reagent_list.update_reagent('Na',222)
    reagent_list.update_reagent('Ast',233)

    reagent_list.update_reagent('Alb',333)

    print reagent_list

def test2():
    reagent_list = ReagentDict()
    path_to_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\LOG\APP'
    reagent_list.build_test_code_dictionary_from_file(path_to_log_folder)
    print reagent_list


if __name__ == '__main__':
    test2()