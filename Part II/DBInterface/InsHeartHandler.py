from DBTables import *

class InsHeartHandler(object):
    """
    """
    def __init__(self):
        pass

    @staticmethod
    def fetch_unsent_items_from_InsHeart(cursor):
        unsent_ins_hearts = []
        if cursor:
            cursor.execute("SELECT * FROM InsHeart WHERE Sent = 0")
            rows = cursor.fetchall()
            for row in rows:
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
                unsent_ins_hearts.append(heart)
                #print 'get one heart:'
                #print heart
        #print unsent_ins_hearts
        return unsent_ins_hearts

    @staticmethod
    def set_inshearts_as_sent(hearts,cursor,connect):
        for heart in hearts:
            if cursor and connect and isinstance(heart,ins_heart):
                cursor.execute("UPDATE InsHeart SET Sent = 1 WHERE ID = {0}".format(heart.ID))
                connect.commit()


