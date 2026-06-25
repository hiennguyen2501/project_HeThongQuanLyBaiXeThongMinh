from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDateTime, QTimer, pyqtSignal
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "designer", "check_in.ui")


class ICheckinView:
    def lay_bien_so(self):
        raise NotImplementedError

    def lay_loai_xe(self):
        raise NotImplementedError

    def bao_loi(self, message):
        raise NotImplementedError

    def thong_bao(self, title, message):
        raise NotImplementedError

    def dong_thanh_cong(self):
        raise NotImplementedError


class CheckInDialog(QDialog, ICheckinView):
    yeu_cau_xac_nhan = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._cap_nhat_thoi_gian_vao()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._cap_nhat_thoi_gian_vao)
        self._timer.start(1000)

        self.btn_checkin.clicked.connect(self.yeu_cau_xac_nhan.emit)

    def _cap_nhat_thoi_gian_vao(self):
        self.lbl_thoi_gian_vao.setText(QDateTime.currentDateTime().toString("dd/MM/yyyy HH:mm:ss"))

    def lay_bien_so(self):
        return self.txt_bien_so.text()

    def lay_loai_xe(self):
        return self.cb_loai_xe.currentText()

    def bao_loi(self, message):
        QMessageBox.warning(self, "Lỗi", message)

    def thong_bao(self, title, message):
        QMessageBox.information(self, title, message)

    def dong_thanh_cong(self):
        self.accept()
