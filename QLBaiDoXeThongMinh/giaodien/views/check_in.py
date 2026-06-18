from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
import os

UI_PATH =  os.path.join(os.path.dirname(__file__),"..","designer","check_in.ui" )

class ICheckinView:
    def lay_bien_so(self): raise NotImplementedError
    def lay_loai_xe(self): raise NotImplementedError
    def bao_loi(self, message):raise NotImplementedError
    def bao_thong_tin(self, message):raise NotImplementedError
    def dong_thanh_cong(self):raise NotImplementedError

class CheckInDialog(QDialog):
    yeu_cau_xac_nhan = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._dinh_dang_combo_loai_xe()

        # nút check-in
        self.btn_checkin.clicked.connect(self.yeu_cau_xac_nhan.emit)

    def _dinh_dang_combo_loai_xe(self):
        self.cb_loai_xe.setStyleSheet("""
QComboBox {
    min-height: 38px;
    padding: 6px 12px;
    background: #FFFFFF;
    border: 1px solid #C8D2DE;
    border-radius: 6px;
    color: #050505;
    font-size: 14px;
}
QComboBox:focus {
    border: 1px solid #2563EB;
}
QComboBox QAbstractItemView {
    background: #FFFFFF;
    color: #050505;
    selection-background-color: #DCEBFF;
    selection-color: #050505;
    border: 1px solid #C8D2DE;
    outline: 0;
}
""")
        self.cb_loai_xe.view().setStyleSheet("""
QListView {
    background: #FFFFFF;
    color: #050505;
    selection-background-color: #DCEBFF;
    selection-color: #050505;
    border: 1px solid #C8D2DE;
    padding: 4px;
}
QListView::item {
    min-height: 30px;
    padding: 6px 10px;
    color: #050505;
}
QListView::item:selected,
QListView::item:hover {
    background: #DCEBFF;
    color: #050505;
}
""")

    def lay_bien_so(self):
        return self.txt_bien_so.text()
    
    def lay_loai_xe(self):
        return self.cb_loai_xe.currentText()
    
    def bao_loi(self, message):
        QMessageBox.warning(self, "Error", message)

    def bao_thong_tin(self, message):
        QMessageBox.information(self, "Thông báo", message)

    def dong_thanh_cong(self):
        self.accept()
    
    
