from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

import sys
import os

UI_PATH =  os.path.join(os.path.dirname(__file__),"..","designer","trang_chu.ui" )

class ITrangChuView():
    """lớp interface"""
    def hien_so_xe(self, xe_may, oto): 
        raise NotImplementedError
    
    def hien_doanh_thu(self, doanh_thu): 
        raise NotImplementedError
    
    def hien_xe_cho(self, so_xe_may_cho, so_xe_oto_cho): 
        raise NotImplementedError
        
class TrangChu(QMainWindow, ITrangChuView):

    yeu_cau_checkin = pyqtSignal()

    def __init__(self):
        super().__init__()
    
        uic.loadUi(UI_PATH, self)
        self._noi_nut()
        

    def _noi_nut(self):
        self.btn_checkin.clicked.connect(self.yeu_cau_checkin.emit)

    
        # function này là 1 logic đúng không ... nên là mình sẽ chuyển nó sang presenter 
        #view chỉ có nhiệm vụ mapping nút thôi không xử lý logic, sau này lỡ có muốn bổ sung nhiều logic hơn thì xử lý chõ khác 

    def hien_so_xe(self, xe_may, oto):
        self.lbl_xe_may_2.setText(str(xe_may))  
        self.lbl_o_to_2.setText(str(oto))

    def hien_doanh_thu(self, doanh_thu):
        self.lbl_doanh_thu.setText(str(doanh_thu))

    def hien_xe_cho(self, so_xe_may_cho, so_xe_oto_cho):
        self.lbl_xe_may_cho.setText(str(so_xe_may_cho))
        self.lbl_o_to_cho.setText(str(so_xe_oto_cho))





