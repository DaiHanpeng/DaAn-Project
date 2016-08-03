import xmlrpclib

class RpcClient():
    """
    rpc framework client.
    """
    def __init__(self):
        self.server_proxy = xmlrpclib.ServerProxy(uri='http://localhost:8000',allow_none=True)

    def fire_reagent_notification(self):
        try:
            self.server_proxy.reagent_handler()
        except Exception as ex:
            print ex

    def fire_order_result_notification(self):
        try:
            self.server_proxy.order_result_handler()
        except Exception as ex:
            print ex

    def fire_calibration_notification(self):
        try:
            self.server_proxy.calibration_handler()
        except Exception as ex:
            print ex

    def fire_control_notification(self):
        try:
            self.server_proxy.control_handler()
        except Exception as ex:
            print ex

    def fire_instrument_log_notificaion(self):
        try:
            self.server_proxy.instrument_log_handler()
        except Exception as ex:
            print ex

    def fire_instrument_status_notificaion(self):
        try:
            self.server_proxy.instrument_status_handler()
        except Exception as ex:
            print ex

def test():
    rpc_client = RpcClient()
    rpc_client.fire_order_result_notification()

if __name__ == '__main__':
    test()