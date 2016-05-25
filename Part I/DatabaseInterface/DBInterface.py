﻿import sqlite3
import os,sys

from ReagentLogParser.ReagentDef import ReagentDict
from MtdResultInfoParser.MtdResultParser import ResultInfo,MtdResultParser
from PdfResultInfoMiner.ReviewAndEditInfoMiner import ReviewAndEditInfoMiner
from PdfResultInfoMiner.OrderResultStruct import *
from PrintedReagentParser.PrintedReagentParser import PrintedReagentInfoItem,PrintedReagentInfoParser

from DBTables import *

SQLITE_DB_PATH = r'D:\DaAn\DaAn-Project\DaAn.db'

class DBInterface(object):
    """

    """
    def __init__(self):
        self.connect = None
        self.cursor = None

    def db_connect_initialize(self,db_path):
        self.connect = sqlite3.connect(db_path)
        with self.connect:
            self.connect.row_factory = sqlite3.Row
            self.cursor = self.connect.cursor()

    def put_reagent_info(self, reagent_info):
        if isinstance(reagent_info,ReagentDict):
            for key in reagent_info.reagent_dict.keys():
                db_insert = "insert into InsReagentInfo (RemainderCount,TestCode,TestName,Sent) values (?,?,?,0)"
                self.cursor.execute(db_insert, [reagent_info.reagent_dict[key], key, key])
                self.connect.commit()

    def put_printed_reagent_info(self,printed_reagent_info):
        if isinstance(printed_reagent_info,PrintedReagentInfoParser):
            self.cursor.execute("delete from InsReagentInfo")
            for reagent_info in printed_reagent_info.reagent_info_list:
                if isinstance(reagent_info,PrintedReagentInfoItem):
                    #R1
                    if reagent_info.r1_position:
                        db_insert = "insert into InsReagentInfo (Position,RemainderCount,TestCode,TestName,Sent,Type) values (?,?,?,?,0,'R1')"
                        self.cursor.execute(db_insert,\
                    [reagent_info.r1_position, reagent_info.r1_count, reagent_info.reagent_name,reagent_info.reagent_name])
                    #R2
                    if reagent_info.r2_position:
                        db_insert = "insert into InsReagentInfo (Position,RemainderCount,TestCode,TestName,Sent,Type) values (?,?,?,?,0,'R2')"
                        self.cursor.execute(db_insert,\
                    [reagent_info.r2_position, reagent_info.r2_count, reagent_info.reagent_name,reagent_info.reagent_name])
                    #Total reagent
                    db_insert = "insert into InsReagentInfo (RemainderCount,TestCode,TestName,Sent,Type) values (?,?,?,0,'Total')"
                    self.cursor.execute(db_insert,\
                [reagent_info.total_count, reagent_info.reagent_name,reagent_info.reagent_name])
                    #commit to database.
                    self.connect.commit()

    def put_mtd_result_info(self, result_info):
        if isinstance(result_info,MtdResultParser):
            for result in result_info.result_list:
                if isinstance(result,ResultInfo):
                    db_insert = "insert into InsTest (Barcode,TestCode,ResultValue,Unit,Absorbance,Sent) values (?,?,?,?,?,0)"
                    self.cursor.execute(db_insert, [result.sample_id, result.test_name, result.value, result.unit, result.abs])
                    self.connect.commit()

    def put_pdf_result_info(self, result_info):
        if isinstance(result_info,ReviewAndEditInfoMiner):
            if result_info.order_result_list:
                for page_result in result_info.order_result_list.order_result_info_list:
                    if isinstance(page_result,OrderResultInfoPerPage):
                        for result in page_result.order_result_info_list:
                            if isinstance(result,OrderResultStruct):
                                for result_item in result.order_result_list:
                                    if isinstance(result_item,OrderResultPair):
                                        db_insert = "insert into InsTest (Barcode,TestCode,ResultValue,Sent) values (?,?,?,0)"
                                        self.cursor.execute(db_insert, [result.sample_id, result_item.order, result_item.result])
                                        self.connect.commit()

    def db_disconnect(self):
        if self.connect:
            self.connect.close()

def test():
    db_interface = DBInterface()

    db_interface.db_connect_initialize(SQLITE_DB_PATH)

    try:
        '''
        heart = db_interface.fetch_one_unsent_item_from_InsHeart()
        if heart:
            print 'get one heart record,'
            print 'TempIncubation:' + str(heart.TempIncubation)
            db_interface.set_insheart_as_sent(heart)
        '''

        '''
        reagent_list = ReagentDict()
        path_to_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\LOG\APP'
        reagent_list.build_test_code_dictionary_from_file(path_to_log_folder)
        print reagent_list

        db_interface.put_reagent_info(reagent_list)
        '''

        '''
        mtd_parser = MtdResultParser()
        mtd_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\A002\DATA'
        mtd_parser.build_result_info_from_mtd_file(mtd_path,None)
        print mtd_parser

        db_interface.put_mtd_result_info(mtd_parser)
        '''

        '''
        pdf_folder_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\05_DaAn\Advia2400_ScreenCapture'
        pdf_file_name = 'Review_And_Edit.pdf'
        pdf_miner = ReviewAndEditInfoMiner(os.path.join(pdf_folder_path,pdf_file_name))
        pdf_miner.extract_info()
        print pdf_miner

        db_interface.put_pdf_result_info(pdf_miner)
        '''

        reagent_parser = PrintedReagentInfoParser()
        file_path = r'..\Advia2400_ScreenCapture'
        reagent_parser.extract_info_from_printed_file(file_path)
        db_interface.put_printed_reagent_info(reagent_parser)
        print reagent_parser


    except Exception as ex:
        print ex

    db_interface.db_disconnect()
    #input('press any key to continue...')

if __name__ == '__main__':
    test()