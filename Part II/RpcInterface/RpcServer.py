import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

from DBInterface.DBTables import *
from DBInterface.SqliteInterface import SqliteInterface
from DaAnInterface.DaAnInterface import DaAnInterface


class MessageHandler():
    """
    """
    def __init__(self):
        pass

    def reagent_handler(self):
        print 'reagent handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                reagents = db_interface.fetch_unsent_items_from_InsReagentInfo()
                if reagents:
                    ##
                    print 'get unsent ins reagent info records,'
                    for reagent in reagents:
                        if isinstance(reagent,ins_reagent_info):
                            print reagent
                    ## reagent info processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_reagent_info(reagents)
                    ##
                    db_interface.set_InsReagentInfos_as_sent(reagents)
            except Exception as ex:
                print ex

    def order_result_handler(self):
        print 'order result handler is triggered...'
        with SqliteInterface() as db_interface:
            try:
                tests = db_interface.fetch_unsent_items_from_InsTest()
                if tests:
                    ##
                    print 'get unsent ins test info records,'
                    for test in tests:
                        if isinstance(test,ins_test):
                            print test
                    ## reagent info processing...
                    daan_interface = DaAnInterface()
                    daan_interface.send_order_result_info(tests)
                    ##
                    db_interface.set_InsTests_as_sent(tests)
            except Exception as ex:
                print ex

    def calibration_handler(self):
        pass

    def control_handler(self):
        pass

def test():
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_introspection_functions()
    server.register_instance(MessageHandler())
    server.serve_forever()
    input('should not be here ...')

if __name__  == '__main__':
    test()
