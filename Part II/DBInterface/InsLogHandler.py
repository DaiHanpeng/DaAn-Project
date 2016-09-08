from DBTables import *

class InsLogHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsLog(cursor):
        unsent_ins_logs = []
        count = 0
        if cursor:
            cursor.execute("SELECT * FROM InsLog WHERE Sent = 0")
            rows = cursor.fetchall()
            print 'fetched unsent records: ' + str(len(rows))

            for row in rows:
                try:
                    instr_log = ins_log()
                    instr_log.Content = row['Content']
                    if "1" == row['LogType']:
                        instr_log.LogType = LogType.Normal
                    elif "2" == row['LogType']:
                        instr_log.LogType = LogType.Warning
                    elif "3" == row['LogType']:
                        instr_log.LogType = LogType.Exception
                    instr_log.RunDate = DateTime.Parse(row['RunDate'])
                    #instr_log.RunDate = DateTime.Now
                    instr_log.ID = row['ID']
                    instr_log.Sent = row['Sent']
                    # add to unsent list
                    unsent_ins_logs.append(instr_log)
                except Exception as ex:
                    print ex
        else:
            print 'cousor error!'

        return unsent_ins_logs

    @staticmethod
    def set_InsLogs_as_sent(instr_logs,cursor,connect):
        for log_item in instr_logs:
            if cursor and connect and isinstance(log_item,ins_log):
                print 'instrument log record sent:'
                print log_item
                cursor.execute("UPDATE InsLog SET Sent = 1 WHERE ID = {0}".format(log_item.ID))
                connect.commit()

def test():
    str_type = str(LogType.Warning)

    print str_type

if __name__ == '__main__':
    test()


