from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

import sys
import os

UI_PATH =  os.path.join(os.path.dirname(__file__),"..","designer","trang_chu.ui" )

class ITrangChuView():
    def hien_so_xe(self, xe_may, oto):
        raise NotImplementedError

    def hien_doanh_thu(self, doanh_thu):
        raise NotImplementedError

    def hien_xe_cho(self, so_xe_may_cho, so_xe_oto_cho):
        raise NotImplementedError

class TrangChu(QMainWindow, ITrangChuView):

    yeu_cau_checkin = pyqtSignal()
    yeu_cau_checkout = pyqtSignal()
    yeu_cau_quan_ly_bai_xe = pyqtSignal()
    yeu_cau_thong_ke_chi_tiet = pyqtSignal()
    yeu_cau_so_do = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_PATH, self)
        self._noi_nut()


    def _noi_nut(self):
        self.btn_checkin.clicked.connect(self.yeu_cau_checkin.emit)
        self.btn_checkout.clicked.connect(self.yeu_cau_checkout.emit)
        self.btn_quan_ly_bai_xe.clicked.connect(self.yeu_cau_quan_ly_bai_xe.emit)
        self.btn_thong_ke_chi_tiet.clicked.connect(self.yeu_cau_thong_ke_chi_tiet.emit)
        self.btn_so_do_b1.clicked.connect(lambda: self.yeu_cau_so_do.emit(0))
        self.btn_so_do_b2.clicked.connect(lambda: self.yeu_cau_so_do.emit(1))


    def hien_so_xe(self, xe_may, oto):
        self.lbl_xe_may_2.setText(str(xe_may))
        self.lbl_o_to_2.setText(str(oto))

    def hien_doanh_thu(self, doanh_thu):
        self.lbl_doanh_thu.setText(f"{doanh_thu:,}".replace(",", ".") + " đ")

    def hien_xe_cho(self, so_xe_may_cho, so_xe_oto_cho):
        self.lbl_xe_may_cho.setText(str(so_xe_may_cho))
        self.lbl_o_to_cho.setText(str(so_xe_oto_cho))

    def hien_ty_le_lap_day(self, so_xe_dang_gui, tong_so_o, ty_le):
        if hasattr(self, "donutLabel"):
            self.donutLabel.setText(f"{ty_le:.2f}%\n{so_xe_dang_gui} / {tong_so_o}")
