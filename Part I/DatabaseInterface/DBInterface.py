import sqlite3
import os,sys

from ReagentLogParser.ReagentDef import ReagentDict
from MtdResultInfoParser.MtdResultParser import ResultInfo,MtdResultParser
from PdfResultInfoMiner.ReviewAndEditInfoMiner import ReviewAndEditInfoMiner
from PdfResultInfoMiner.OrderResultStruct import *

from DBTables import *

SQLITE_DB_PATH = 'DaAn.db'

class DBInterface(object):
    connect = None
    cursor = None

    @classmethod
    def db_connect_initialize(cls):
        cls.connect = sqlite3.connect(SQLITE_DB_PATH)
        with cls.connect:
            cls.connect.row_factory = sqlite3.Row
            cls.cursor = cls.connect.cursor()

    @classmethod
    def fetch_one_unsent_item_from_InsHeart(cls):
        if cls.cursor:
            cls.cursor.execute("SELECT * FROM InsHeart WHERE Sent = 0")
            row = cls.cursor.fetchone()
            if row:
                heart = ins_heart()
                #heart.RunDate =  DateTime.Parse(row['RunDate'])
                heart.TempReagent = row['TempReagent']
                heart.TempIncubation = row['TempIncubation']
                heart.CleaningFluid = row['CleaningFluid']
                heart.Detergent = row['Detergent']
                heart.Effluent = row['Effluent']
                heart.Temperature = row['Temperature']
                heart.SubstrateA = row['SubstrateA']
                heart.SubstrateB = row['SubstrateB']
                heart.PositivePressure = row['PositivePressure']
                heart.NegativePressure = row['NegativePressure']
                heart.ID = row['ID']
                return heart
        return None

    @classmethod
    def set_insheart_as_sent(cls,heart):
        if cls.cursor and cls.connect and isinstance(heart,ins_heart):
            cls.cursor.execute("UPDATE InsHeart SET Sent = 1 WHERE ID = {0}".format(heart.ID))
            cls.connect.commit()
            return True
        return False

    @classmethod
    def fetch_one_unsent_item_from_InsLog(cls):
        pass


    @classmethod
    def put_reagent_info(cls,reagent_info):
        if isinstance(reagent_info,ReagentDict):
            for key in reagent_info.reagent_dict.keys():
                db_insert = "insert into InsReagentInfo (RemainderCount,TestCode,TestName,Sent) values (?,?,?,0)"
                cls.cursor.execute(db_insert,[reagent_info.reagent_dict[key],key,key])
                cls.connect.commit()

    @classmethod
    def put_mtd_result_info(cls,result_info):
        if isinstance(result_info,MtdResultParser):
            for result in result_info.result_list:
                if isinstance(result,ResultInfo):
                    db_insert = "insert into InsTest (Barcode,TestCode,ResultValue,Unit,Absorbance,Sent) values (?,?,?,?,?,0)"
                    cls.cursor.execute(db_insert,[result.sample_id,result.test_name,result.value,result.unit,result.abs])
                    cls.connect.commit()

    @classmethod
    def put_pdf_result_info(cls,result_info):
        if isinstance(result_info,ReviewAndEditInfoMiner):
            if result_info.order_result_list:
                for page_result in result_info.order_result_list.order_result_info_list:
                    if isinstance(page_result,OrderResultInfoPerPage):
                        for result in page_result.order_result_info_list:
                            if isinstance(result,OrderResultStruct):
                                for result_item in result.order_result_list:
                                    if isinstance(result_item,OrderResultPair):
                                        db_insert = "insert into InsTest (Barcode,TestCode,ResultValue,Sent) values (?,?,?,0)"
                                        cls.cursor.execute(db_insert,[result.sample_id,result_item.order,result_item.result])
                                        cls.connect.commit()

    @classmethod
    def db_disconnect(cls):
        if cls.connect:
            cls.connect.close()

def test():
    DBInterface.db_connect_initialize()

    try:
        '''
        heart = DBInterface.fetch_one_unsent_item_from_InsHeart()
        if heart:
            print 'get one heart record,'
            print 'TempIncubation:' + str(heart.TempIncubation)
            DBInterface.set_insheart_as_sent(heart)
        '''

        '''
        reagent_list = ReagentDict()
        path_to_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\LOG\APP'
        reagent_list.build_test_code_dictionary_from_file(path_to_log_folder)
        print reagent_list

        DBInterface.put_reagent_info(reagent_list)
        '''


        mtd_parser = MtdResultParser()
        mtd_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\DATA'
        mtd_parser.build_result_info_from_mtd_file(mtd_path,None)
        print mtd_parser

        DBInterface.put_mtd_result_info(mtd_parser)


        '''
        pdf_folder_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\Advia2400_ScreenCapture'
        pdf_file_name = 'Review_And_Edit.pdf'
        pdf_miner = ReviewAndEditInfoMiner(os.path.join(pdf_folder_path,pdf_file_name))
        pdf_miner.extract_info()
        print pdf_miner

        DBInterface.put_pdf_result_info(pdf_miner)
        '''

    except Exception as ex:
        print ex

    DBInterface.db_disconnect()
    #input('press any key to continue...')

if __name__ == '__main__':
    test()