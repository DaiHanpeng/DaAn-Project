from DBTables import *

class InsStatusHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsStatus(cursor):
        unsent_ins_status = []
        if cursor:
            cursor.execute("SELECT * FROM InsStatus WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                try:
                    instr_status = ins_status()
                    #instr_status.RunDate = DateTime.Parse(row['RunDate'])
                    instr_status.RunDate = DateTime.Now
                    if "0" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.START
                    elif "1" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.PAUSE
                    elif "2" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.STOP
                    elif "3" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.FINISHED
                    elif "4" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.POWER_ON
                    elif "5" == row['StatusCode']:
                        instr_status.StatusCode = StatusType.POWER_OFF
                    else:
                        continue
                    instr_status.ID = row['ID']
                    instr_status.Sent = row['Sent']
                    # add to unsent list
                    unsent_ins_status.append(instr_status)
                except Exception as ex:
                    print ex
        return unsent_ins_status

    @staticmethod
    def set_InsStatus_as_sent(instr_status,cursor,connect):
        for status_item in instr_status:
            if cursor and connect and isinstance(status_item,ins_status):
                print 'instrument status record sent:'
                print status_item
                cursor.execute("UPDATE InsStatus SET Sent = 1 WHERE ID = {0}".format(status_item.ID))
                connect.commit()


