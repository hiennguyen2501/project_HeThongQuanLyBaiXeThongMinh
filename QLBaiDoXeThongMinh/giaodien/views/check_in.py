from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
import os

UI_PATH =  os.path.join(os.path.dirname(__file__),"..","designer","check_in.ui" )

class ICheckinView:
    def lay_bien_so(self): raise NotImplementedError
    def lay_loai_xe(self): raise NotImplementedError
    def bao_loi(self, message):raise NotImplementedError
    def dong_thanh_cong(self):raise NotImplementedError

class CheckInDialog(QDialog):
    yeu_cau_xac_nhan = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)

        # nút check-in
        self.btn_checkin.clicked.connect(self.yeu_cau_xac_nhan.emit)

    def lay_bien_so(self):
        return self.txt_bien_so.text()
    
    def lay_loai_xe(self):
        return self.cb_loai_xe.currentText()
    
    def bao_loi(self, message):
        QMessageBox.warning(self, "Error", message)

    def dong_thanh_cong(self):
        self.accept()
    
    