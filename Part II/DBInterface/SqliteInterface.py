import clr
import sqlite3

from DBTables import *
from InsHeartHandler import *

clr.AddReferenceToFileAndPath('IronPython.SQLite.dll')

#Attention:
#The SQLITE_DB_PATH is related to path of <IronPython.SQLite.dll>.
SQLITE_DB_PATH = r'D:\DaAn\DaAn-Project\Part II\DaAn.db'

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

    def fetch_unsent_items_from_InsHeart(self):
        return InsHeartHandler.fetch_unsent_items_from_InsHeart(self.cursor)
    
    def set_inshearts_as_sent(self,hearts):
        return InsHeartHandler.set_inshearts_as_sent(hearts,self.cursor,self.connect)
    
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


