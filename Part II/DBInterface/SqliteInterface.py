import clr
import sqlite3

from DBTables import *
from InsHeartHandler import *

clr.AddReferenceToFileAndPath('IronPython.SQLite.dll')

#Attention:
#The SQLITE_DB_PATH is related to path of <IronPython.SQLite.dll>.
SQLITE_DB_PATH = r'S:\DaAn.db'
#SQLITE_DB_PATH = r'D:\DaAn\DaAnGit\DaAn-Project\Part II\DaAn.db'

from InsHeartHandler import InsHeartHandler
from InsReagentInfoHandler import InsReagentInfoHandler
from InsTestHandler import InsTestHandler
from InsCalibrationResultHandler import InsCalibrationResultHandler
from InsQCHandler import InsQCHandler
from InsLogHandler import InsLogHandler
from InsStatusHandler import InsStatusHandler


class SqliteInterface(object):
    def __init__(self):
        self.connect = None
        self.cursor = None

    def __enter__(self):
        print 'start sqlite db initializae...'
        self.db_connect_initialize()
        return self

    def db_connect_initialize(self):
        self.connect = sqlite3.connect(SQLITE_DB_PATH)
        if self.connect:
            print 'DB connected OK．'
            self.connect.row_factory = sqlite3.Row
            self.cursor = self.connect.cursor()

    # InsHeart Interface...
    def fetch_unsent_items_from_InsHeart(self):
        return InsHeartHandler.fetch_unsent_items_from_InsHeart(self.cursor)
    
    def set_inshearts_as_sent(self,hearts):
        return InsHeartHandler.set_inshearts_as_sent(hearts,self.cursor,self.connect)

    #InsReagentInfo Interface...
    def fetch_unsent_items_from_InsReagentInfo(self):
        return InsReagentInfoHandler.fetch_unsent_items_from_InsReagentInfo(self.cursor)
    
    def set_InsReagentInfos_as_sent(self,reagents):
        return InsReagentInfoHandler.set_InsReagentInfos_as_sent(reagents,self.cursor,self.connect)

    #InsTest Interface...
    def fetch_unsent_items_from_InsTest(self):
        return InsTestHandler.fetch_unsent_items_from_InsTest(self.cursor)
    
    def set_InsTests_as_sent(self,tests):
        return InsTestHandler.set_InsTests_as_sent(tests,self.cursor,self.connect)

    #InsCalibrationResult Interface...
    def fetch_unsent_items_from_InsCalibrationResult(self):
        return InsCalibrationResultHandler.fetch_unsent_items_from_InsCalibrationResult(self.cursor)
    
    def set_InsCalibrationResults_as_sent(self,cal_results):
        return InsCalibrationResultHandler.set_InsCalibrationResults_as_sent(cal_results,self.cursor,self.connect)

    #InsQC Interface...
    def fetch_unsent_items_from_InsQC(self):
        return InsQCHandler.fetch_unsent_items_from_InsQC(self.cursor)
    
    def set_InsQCs_as_sent(self,ins_qcs):
        return InsQCHandler.set_InsQCs_as_sent(ins_qcs,self.cursor,self.connect)

    #InsLog Interface...
    def fetch_unsent_items_from_InsLog(self):
        return InsLogHandler.fetch_unsent_items_from_InsLog(self.cursor)
    
    def set_InsLogs_as_sent(self,ins_logs):
        return InsLogHandler.set_InsLogs_as_sent(ins_logs,self.cursor,self.connect)

    #InsStatus Interface...
    def fetch_unsent_items_from_InsStatus(self):
        return InsStatusHandler.fetch_unsent_items_from_InsStatus(self.cursor)
    
    def set_InsStatus_as_sent(self,ins_status):
        return InsStatusHandler.set_InsStatus_as_sent(ins_status,self.cursor,self.connect)


 
    def __exit__(self,_type,value,traceback):
        self.db_disconnect()
        print 'db disconnectted...'

    def db_disconnect(self):
        if self.connect:
            return self.connect.close()

if __name__ == '__main__':  
    with SqliteInterface() as db_interface:
        print 'testing start...'
        print db_interface
        try:
            hearts = db_interface.fetch_unsent_items_from_InsHeart()
            if hearts:
                print 'get unsent insheart records,'
                for heart in hearts:
                    if isinstance(heart,ins_heart):
                        print heart
                db_interface.set_inshearts_as_sent(hearts)
        except Exception as ex:
            print ex
 
    '''
    db_interface = SqliteInterface()

    print 'testing start...'
    print db_interface
    try:
        db_interface.db_connect_initialize()
        hearts = db_interface.fetch_unsent_items_from_InsHeart()
        print hearts
        if hearts:
            print 'get unsent insheart records,'
            for heart in hearts:
                if isinstance(heart,ins_heart):
                    print heart
            db_interface.set_inshearts_as_sent(hearts)
    except Exception as ex:
        print ex
    finally:
        db_interface.db_disconnect()
    '''
    
    input('press any key to continue...')


