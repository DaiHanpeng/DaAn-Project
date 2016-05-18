import clr

clr.AddReferenceToFileAndPath('IronPython.SQLite.dll')

import sqlite3

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
                heart.RunDate =  DateTime.Parse(row['RunDate'])
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
    def db_disconnect(cls):
        if cls.connect:
            cls.connect.close()

if __name__ == '__main__':
    DBInterface.db_connect_initialize()

    print 'testing start...'
    try:
        heart = DBInterface.fetch_one_unsent_item_from_InsHeart()
        if heart:
            print 'get one heart record,'
            print 'TempIncubation:' + str(heart.TempIncubation)
            DBInterface.set_insheart_as_sent(heart)
    except Exception as ex:
        print ex

    DBInterface.db_disconnect()
    input('press any key to continue...')


