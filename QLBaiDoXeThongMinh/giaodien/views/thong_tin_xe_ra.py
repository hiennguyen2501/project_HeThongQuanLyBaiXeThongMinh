from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "designer", "thong_tin_xe_ra.ui")


class ThongTinXeRaDialog(QDialog):
    yeu_cau_xuat_hoa_don = pyqtSignal(str)

    def __init__(self, bien_lai):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._bien_lai = bien_lai
        self._hien_bien_lai(bien_lai)
        self.btn_in_ve.clicked.connect(self._chon_noi_luu)

    def thong_bao(self, title, message):
        QMessageBox.information(self, title, message)

    def bao_loi(self, message):
        QMessageBox.warning(self, "Loi", message)

    def _hien_bien_lai(self, bien_lai):
        xe_ra = bien_lai["xe_ra"]
        so_phut = int(bien_lai["so_phut_gui"])
        self.lbl_bien_so.setText(xe_ra.bien_so)
        self.lbl_loai_xe.setText("Xe may" if xe_ra.loai_xe == "XeMay" else "O to")
        self.lbl_vi_tri_do.setText(bien_lai["ma_vi_tri"])
        self.lbl_gio_vao.setText(xe_ra.thoi_gian_vao.strftime("%d/%m/%Y %H:%M"))
        self.lbl_gio_ra.setText(bien_lai["thoi_gian_ra"].strftime("%d/%m/%Y %H:%M"))
        self.lbl_thoi_gian_gui.setText(f"{so_phut // 60} gio {so_phut % 60} phut")
        self.lbl_thanh_tien.setText(f"{bien_lai['tien_gui']:,}".replace(",", ".") + " d")

    def _chon_noi_luu(self):
        xe_ra = self._bien_lai["xe_ra"]
        ten_file = f"hoa_don_{xe_ra.bien_so}".replace(" ", "_").replace("/", "_").replace("\\", "_")
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Luu anh hoa don",
            f"{ten_file}.png",
            "PNG Image (*.png)",
        )
        if file_path:
            if not file_path.lower().endswith(".png"):
                file_path += ".png"
            self.yeu_cau_xuat_hoa_don.emit(file_path)
