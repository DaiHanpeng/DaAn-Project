import xmlrpclib

class RpcClient():
    """
    rpc framework client.
    """
    def __init__(self):
        self.server_proxy = xmlrpclib.ServerProxy('http://localhost:8000')

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
        pass

    def fire_control_notification(self):
        pass


def test():
    rpc_client = RpcClient()
    rpc_client.fire_order_result_notification()

if __name__ == '__main__':
    test()