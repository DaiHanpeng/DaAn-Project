from PdfMinerWrapper import *
from OrderResultStruct import OrderResultPair,OrderResultStruct,PageOrderResultInfo,OrderResultInfoPerPage,OrderResultInfoAll


class ReviewAndEditInfoMiner(object):
    """
    extract order and result information in pdf file.
    """
    def __init__(self, pdf_doc, pdf_pwd=""):
        self._pdf_doc = pdf_doc
        self._pdf_pwd = pdf_pwd
        self._order_list = []
        self._result_list = []
        self.order_result_list = OrderResultInfoAll()

    def extract_info(self):
        with PdfMinerWrapper(self._pdf_doc,self._pdf_pwd) as doc:
            for page in doc:
                sample_id_list = []
                date_time_list = []
                page_order_result = PageOrderResultInfo()
                for tbox in page:
                    if isinstance(tbox, LTTextBox):
                        for obj in tbox:
                            text = str(obj.get_text())
                            text = text.replace('\n','')
                            if isinstance(text,str):
                                if len(text) >= 8 and text.isdigit():
                                    sample_id_list.append(text)
                                elif -1 <> text.find(':') and -1 <> text.find('/'):
                                    date_time_list.append(text)
                                elif len(text) < 8 and -1 == text.find(':'):
                                    page_order_result.update_order_result_list(x0=tbox.x0,value=text)

                page_order_result_info  = OrderResultInfoPerPage(page.pageid,sample_id_list,date_time_list,page_order_result)
                page_order_result_info.construct_order_result_info_list()
                self.order_result_list.append_page_order_result_info(page_order_result_info)

    def __repr__(self):
        return repr(self.order_result_list)


def test():
    pdf_miner = ReviewAndEditInfoMiner('Review_And_Edit.pdf')
    pdf_miner.extract_info()
    print pdf_miner


if __name__ == '__main__':
    test()
