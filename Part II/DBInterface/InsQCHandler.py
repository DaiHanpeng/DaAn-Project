from DBTables import *

class InsQCHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsQC(cursor):
        unsent_ins_qcs = []
        if cursor:
            cursor.execute("SELECT * FROM InsQC WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                qc = ins_qc()
                qc.Absorbance = row['Absorbance']
                qc.Barcode = row['Barcode']
                qc.ExpireDate = DateTime.Parse(row['ExpireDate'])
                qc.LotNo = row['LotNo']
                qc.Name = row['Name']
                qc.OneSD = row['OneSD']
                qc.OpenDate = DateTime.Parse(row['OpenDate'])
                #qc.OpenValidDays = row['OpenValidDays']
                qc.ReagentLotNo = row['ReagentLotNo']
                qc.ResultDate = DateTime.Parse(row['ResultDate'])
                qc.ResultValue = row['ResultValue']
                qc.TargetValue = row['TargetValue']
                qc.TestCode = row['TestCode']
                #qc.Type = row['Type']
                qc.Unit = row['Unit']
                qc.Sent = row['Sent']
                qc.ID = row['ID']
                #qc.SentDate = row['SentDate']
                unsent_ins_qcs.append(qc)
        return unsent_ins_qcs

    @staticmethod
    def set_InsQCs_as_sent(ins_qcs,cursor,connect):
        for qc in ins_qcs:
            if cursor and connect and isinstance(qc,ins_qc):
                cursor.execute("UPDATE InsQC SET Sent = 1 WHERE ID = {0}".format(qc.ID))
                connect.commit()


