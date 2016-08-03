from DBTables import *

class InsReagentInfoHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsReagentInfo(cursor):
        unsent_ins_reagents = []
        if cursor:
            cursor.execute("SELECT * FROM InsReagentInfo WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                reagent = ins_reagent_info()
                reagent.AuthorizeCount = row['AuthorizeCount']
                reagent.LotNo = row['LotNo']                   
                reagent.Position = row['Position']
                if row['RemainderCount']:
                    reagent.RemainderCount = int(row['RemainderCount'])
                else:
                    reagent.RemainderCount = 0
                reagent.RemainderValue = row['RemainderValue']
                reagent.TestCode = row['TestCode']
                reagent.TestName = row['TestName']
                reagent.Type = row['Type']
                reagent.Sent = row['Sent']
                reagent.ID = row['ID']
                unsent_ins_reagents.append(reagent)
        return unsent_ins_reagents

    @staticmethod
    def set_InsReagentInfos_as_sent(ins_reagents,cursor,connect):
        for reagent in ins_reagents:
            if cursor and connect and isinstance(reagent,ins_reagent_info):
                cursor.execute("UPDATE InsReagentInfo SET Sent = 1 WHERE ID = {0}".format(reagent.ID))
                connect.commit()


