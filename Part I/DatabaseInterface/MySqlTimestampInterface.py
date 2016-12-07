import pymysql
from DBTables import table_last_update_timestamp

MYSQL_DB_SCHEMA = r'DaAn'

class TableTimestampInterface(object):
    '''
    Interface for timestamp table.
    '''
    def __init__(self):
        self.connect = None
        self.cursor = None

    def db_connect_initialize(self,db_path):
        #elf.connect = sqlite3.connect(db_path)
        #self.connect = MySQLdb.connect(host='10.10.10.222', user='root',passwd='root')
        #self.connect = MySQLdb.connect(host='192.168.2.106', user='root',passwd='root')
        self.connect = pymysql.connect(host='192.168.0.106', user='root',passwd='root')
        self.connect.select_db(db_path)

        with self.connect:
            #self.connect.row_factory = sqlite3.Row
            self.cursor = self.connect.cursor()
            self.init_table_update_timestamp()

    def init_table_update_timestamp(self):
        #1. create table if not exists.
        #2. insert original records if not exists.
        db_init = '''
        CREATE TABLE  IF NOT EXISTS `table_last_update_timestamp` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `table_name` varchar(24) NOT NULL,
          `update_timestamp` datetime NOT NULL,
          PRIMARY KEY (`id`,`table_name`),
          UNIQUE KEY `id_UNIQUE` (`id`),
          UNIQUE KEY `table_name_UNIQUE` (`table_name`)
        ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
        INSERT INTO table_last_update_timestamp(table_name,update_timestamp) SELECT 'Calibration','2000-01-01 01:01:01' FROM table_last_update_timestamp WHERE NOT EXISTS(SELECT table_name FROM table_last_update_timestamp WHERE table_name='Calibration') LIMIT 1;
        INSERT INTO table_last_update_timestamp(table_name,update_timestamp) SELECT 'Control','2000-01-01 01:01:01' FROM table_last_update_timestamp WHERE NOT EXISTS(SELECT table_name FROM table_last_update_timestamp WHERE table_name='Control') LIMIT 1;
        INSERT INTO table_last_update_timestamp(table_name,update_timestamp) SELECT 'MtdResult','2000-01-01 01:01:01' FROM table_last_update_timestamp WHERE NOT EXISTS(SELECT table_name FROM table_last_update_timestamp WHERE table_name='MtdResult') LIMIT 1;
        INSERT INTO table_last_update_timestamp(table_name,update_timestamp) SELECT 'ErrorReport','2000-01-01 01:01:01' FROM table_last_update_timestamp WHERE NOT EXISTS(SELECT table_name FROM table_last_update_timestamp WHERE table_name='ErrorReport') LIMIT 1;
        INSERT INTO table_last_update_timestamp(table_name,update_timestamp) SELECT 'CalibrationCurve','2000-01-01 01:01:01' FROM table_last_update_timestamp WHERE NOT EXISTS(SELECT table_name FROM table_last_update_timestamp WHERE table_name='CalibrationCurve') LIMIT 1;
        '''

        self.cursor.execute(db_init)
        self.connect.commit()

    def update_table_timestamp(self,table_name,timestamp):
        #print 'table name: ', table_name
        #print 'updated timestamp: ', timestamp
        db_update = "UPDATE table_last_update_timestamp SET update_timestamp = %s WHERE table_name = %s"
        self.cursor.execute(db_update,(timestamp,table_name))
        self.connect.commit()

    def get_table_last_updated_timestamp(self,table_name):
        if isinstance(table_name,str):
            db_query = "SELECT  update_timestamp FROM table_last_update_timestamp WHERE table_name = %s"
            self.cursor.execute(db_query,(table_name,))
            self.connect.commit()
            timestamp = self.cursor.fetchone()
            #print type(timestamp[0])
            #print 'table = ',table_name,'\t updated at: ',timestamp[0]
            return timestamp[0]

    def db_disconnect(self):
        if self.connect:
            self.connect.close()

def test():
    import datetime

    db_interface = TableTimestampInterface()
    db_interface.db_connect_initialize(MYSQL_DB_SCHEMA)
    try:
        a = '2015-12-23 10:21:33'
        b = datetime.datetime.strptime('04 May 2016 08:18:34','%d %b %Y %H:%M:%S')
        c = datetime.datetime.strptime('Sep-21-16 16:34:12','%b-%d-%y %H:%M:%S')
        d = datetime.datetime.strptime('Sep-21-2016 16:34:12','%b-%d-%Y %H:%M:%S')
        e = datetime.datetime.strptime('4/28/2016 08:00:32','%m/%d/%Y %H:%M:%S')

        db_interface.update_table_timestamp('Control',e)
        d1 = db_interface.get_table_last_updated_timestamp('Control')

        d2 = db_interface.get_table_last_updated_timestamp('Calibration')
        print d1
        print d2

        print d1 - d2

    except Exception as ex:
        print ex

    db_interface.db_disconnect()
    #input('press any key to continue...')

if __name__ == '__main__':
    test()
