from DBTables import *

class InsLogHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsLog(cursor):
        unsent_ins_logs = []
        if cursor:
            cursor.execute("SELECT * FROM InsLog WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                try:
                    instr_log = ins_log()
                    instr_log.Content = row['Content']
                    instr_log.LogType = row['LogType']
                    instr_log.RunDate = DateTime.Parse(row['RunDate'])
                    instr_log.ID = row['ID']
                    instr_log.Sent = row['Sent']
                    # add to unsent list
                    unsent_ins_logs.append(instr_log)
                except Exception as ex:
                    print ex
        return unsent_ins_logs

    @staticmethod
    def set_InsLogs_as_sent(instr_logs,cursor,connect):
        for log_item in instr_logs:
            if cursor and connect and isinstance(log_item,ins_log):
                cursor.execute("UPDATE InsLog SET Sent = 1 WHERE ID = {0}".format(log_item.ID))
                connect.commit()


