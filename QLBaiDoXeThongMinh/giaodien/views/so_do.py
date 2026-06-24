from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "designer", "so_do.ui")


class SoDoBaiXeWindow(QMainWindow):
    def __init__(self, tang=0):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.tabWidget.setCurrentIndex(tang)
        if hasattr(self, "btn_quay_ve"):
            self.btn_quay_ve.clicked.connect(self.close)

    def hien_so_do(self, du_lieu_xe_may, du_lieu_oto):
        self._ve_tang(self.gridLayout, du_lieu_xe_may)
        self._ve_tang(self.gridLayout_2, du_lieu_oto)

    def _ve_tang(self, layout, du_lieu_tang):
        self._xoa_layout(layout)
        for row_group, hang_slot in enumerate(du_lieu_tang):
            for index, slot in enumerate(hang_slot):
                button = self._tao_nut_vi_tri(slot)
                hang = row_group
                cot = index + index // 2
                layout.addWidget(button, hang, cot)

    def _tao_nut_vi_tri(self, slot):
        ma_vi_tri = slot["ma_vi_tri"]
        con_trong = slot["trang_thai"] == "Trống" or slot["trang_thai"] == "Trá»‘ng"
        button = QPushButton("\n".join(ma_vi_tri))
        button.setProperty("class", "SlotBtn")
        button.setMinimumSize(58, 72)
        button.setStyleSheet(
            "background-color: #09C56B; color: #050505; border-radius: 8px; font-weight: 900;"
            if con_trong
            else "background-color: #FF3238; color: #050505; border-radius: 8px; font-weight: 900;"
        )
        trang_thai = "Con trong" if con_trong else f"Da co xe\nBien so: {slot['bien_so']}"
        button.clicked.connect(lambda checked=False, vt=ma_vi_tri, tt=trang_thai: self._hien_thong_tin(vt, tt))
        return button

    def _hien_thong_tin(self, ma_vi_tri, trang_thai):
        QMessageBox.information(self, "Thong tin vi tri", f"Vi tri {ma_vi_tri}: {trang_thai}")

    def _xoa_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
