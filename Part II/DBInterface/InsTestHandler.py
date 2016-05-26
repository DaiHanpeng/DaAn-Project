from DBTables import *

class InsTestHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsTest(cursor):
        unsent_ins_tests = []
        if cursor:
            cursor.execute("SELECT * FROM InsTest WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
                test = ins_test()
                test.Absorbance = row['Absorbance']
                test.Barcode = row['Barcode']
                test.ReagentLotNo = row['ReagentLotNo']
                test.RefHigh = row['RefHigh']
                test.RefLow = row['RefLow']
                test.ResultDate = DateTime.Now#row['ResultDate']
                test.ResultValue = row['ResultValue']
                test.SeqNo = row['SeqNo']
                test.TestCode = row['TestCode']
                test.Unit = row['Unit']
                test.ID = row['ID']
                test.Sent = row['Sent']
                #test.SentDate = row['SentDate']
                unsent_ins_tests.append(test)
        return unsent_ins_tests

    @staticmethod
    def set_InsTests_as_sent(ins_tests,cursor,connect):
        for test in ins_tests:
            if cursor and connect and isinstance(test,ins_test):
                cursor.execute("UPDATE InsTest SET Sent = 1 WHERE ID = {0}".format(test.ID))
                connect.commit()


