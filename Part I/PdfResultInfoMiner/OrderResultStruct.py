
"""
///////////////////////////////////////////////////////////////////////////////////////
from the view of Application,
we divide the infomation in below structure:
order and result should be a pair, if only order exists, the result set to none
//////////////////////////////////////////////////////////////////////////////////////
"""
class OrderResultPair(object):
    """
    this paitr is for define the test - result,
    """
    def __init__(self,order,result=''):
        self.order = order
        self.result = result

    def __repr__(self):
        return ('\norder: ' + str(self.order) + ',' + '\t' + 'result: ' + str(self.result))


class OrderResultStruct(object):
    """
    order result should be related to one specify sample id, and one datetime to illustrate the collection datetime.
    """
    def __init__(self, sample_id, date_time='',order_result_list=[]):
        self.sample_id = sample_id
        self.date_time = date_time
        self.order_result_list = order_result_list #list of OrderResultPair

    def update_order_result(self, order_result):
        """
        :param order_result: the record reqiured to be updated.
        :return: none
        :purpose:update the record if it's exist in the list already, oterwise, just apped it into the list.
        """
        if isinstance(order_result,OrderResultPair):
            for item in self.order_result_list:
                if item.order == order_result.order:
                    item.result = order_result.result
                    return
            self.order_result_list.append(order_result)

    def __repr__(self):
        return 'sample id: ' + str(self.sample_id) + '\t' + 'datetime: ' + str(self.date_time) + \
               ''.join(repr(item) for item in self.order_result_list) + '\n'

"""
///////////////////////////////////////////////////////////////////////////////////////
from the view of pdf file.
pdfminer will divide pdf files into blocks, ecery block has its own coordinates.
the most complicated part of the pattern search is how to match the order blocks with it's related result block.
the sequence of orders and results can be in random, while the sammple id and date time should be from left to right.
so i have to compare the block coordinate(x0) to determine the order result sequence and which sample id it belongs to.
///////////////////////////////////////////////////////////////////////////////////////
"""

class OrderResultInfoList():
    """
    list of order result info per sample item.
    """
    def __init__(self,x0,value):
        self.x0 = x0
        self.order_result_list = []
        self.order_result_list.append(value)

    def __repr__(self):
        return 'x0:'+str(self.x0)+'\n' + ''.join(repr(item) for item in self.order_result_list) + '\n'

class PageOrderResultInfo():
    """
    order info lists per page.
    """
    def __init__(self):
        self.page_order_result_list = []

    def update_order_result_list(self,x0,value):
        """
        :param x0: x0 position
        :param value: value of order or result.
        :return:
        """
        for l in self.page_order_result_list:
            if isinstance(l,OrderResultInfoList):
                if x0 == l.x0:
                    l.order_result_list.append(value)
                    return
        new_list = OrderResultInfoList(x0,value)
        self.page_order_result_list.append(new_list)
        self.sort_order_result_list()

    def sort_order_result_list(self):
        self.page_order_result_list.sort(cmp=lambda a,b:cmp(a.x0,b.x0))

    def __repr__(self):
        return 'order result list:\n' + ''.join(repr(item) for item in self.page_order_result_list)


class OrderResultInfoPerPage():
    """
    every page of pdf file should contain 0 - 3 items of order-result info.
    """
    def __init__(self,page_no,sample_id_list=[],date_time_list=[],page_order_result=None):
        self.page_no = page_no
        self._sample_id_list = sample_id_list
        self._date_time_list = date_time_list
        self._order_result_list = []
        if isinstance(page_order_result,PageOrderResultInfo):
            self._order_result_list = page_order_result.page_order_result_list
        self.order_result_info_list = []

    def construct_order_result_info_list(self):
        if (2*len(self._date_time_list) == 2*len(self._sample_id_list) == len(self._order_result_list)):
            while self._sample_id_list:
                order_result_record = OrderResultStruct(sample_id=self._sample_id_list.pop(0),date_time=self._date_time_list.pop(0),order_result_list=[])
                self.order_result_info_list.append(order_result_record)
                order_list = self._order_result_list.pop(0)
                result_list = self._order_result_list.pop(0)
                if isinstance(order_list,OrderResultInfoList) and isinstance(result_list,OrderResultInfoList):
                    if len(order_list.order_result_list) == len(result_list.order_result_list):
                        while order_list.order_result_list and result_list.order_result_list:
                            order_result_pair = OrderResultPair(order_list.order_result_list.pop(0),result_list.order_result_list.pop(0))
                            order_result_record.update_order_result(order_result_pair)


    def __repr__(self):
        return 'page no.'+ str(self.page_no) + ': \n' + ''.join(repr(item)  for item in self.order_result_info_list)



class OrderResultInfoAll():
    """
    order result info all pdf file.
    """
    def __init__(self):
        self.order_result_info_list = []

    def append_page_order_result_info(self,page_order_result_info):
        if isinstance(page_order_result_info,OrderResultInfoPerPage):
            self.order_result_info_list.append(page_order_result_info)

    def __repr__(self):
        return 'All order result info of:\n' + ''.join(repr(item) for item in self.order_result_info_list) + '\n'


def test():
    order_result_Alb = OrderResultPair('Alb','12')
    order_result_Alt = OrderResultPair('Alt','2.5')
    order_result_Ast = OrderResultPair('Ast','122')
    order_result_Na = OrderResultPair('Na','9.9')
    order_result_K = OrderResultPair('K','120')

    order_result_Alb_rerun = OrderResultPair('Alb','999')

    order_result_list = [order_result_Alb,order_result_Alt,order_result_Ast]
    sample_order_result = OrderResultStruct('2233445566','20160511',order_result_list)

    sample_order_result.update_order_result(order_result_Na)
    sample_order_result.update_order_result(order_result_K)

    sample_order_result.update_order_result(order_result_Alb_rerun)

    print sample_order_result


if __name__ == '__main__':
    test()