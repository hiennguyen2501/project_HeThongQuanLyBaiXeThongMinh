from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QMessageBox, QVBoxLayout
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "designer", "check_out.ui")


class CheckOutDialog(QDialog):
    yeu_cau_xac_nhan = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._danh_sach_xe = []
        self._list_goi_y = self._tao_danh_sach_goi_y()
        self.btn_checkout.clicked.connect(self.yeu_cau_xac_nhan.emit)
        self.txt_bien_so.textChanged.connect(self._cap_nhat_goi_y)
        self._list_goi_y.itemClicked.connect(self._chon_goi_y)

    def lay_bien_so(self):
        return self.txt_bien_so.text().strip()

    def hien_danh_sach_goi_y(self, danh_sach_xe):
        self._danh_sach_xe = danh_sach_xe
        self._cap_nhat_goi_y(self.txt_bien_so.text())

    def bao_loi(self, message):
        QMessageBox.warning(self, "Lỗi", message)

    def dong_thanh_cong(self):
        self.accept()

    def _tao_danh_sach_goi_y(self):
        list_goi_y = QListWidget(self)
        list_goi_y.setStyleSheet(
            "QListWidget { background: #FFFFFF; border: 1px solid #C8D2DE;"
            " border-radius: 6px; font-size: 14px; color: #050505; }"
            "QListWidget::item { padding: 8px 12px; }"
            "QListWidget::item:hover { background: #E6EDF6; }"
            "QListWidget::item:selected { background: #176BFF; color: #FFFFFF; }"
        )
        list_goi_y.setMaximumHeight(200)

        card_layout = self.txt_bien_so.parent().layout()
        if card_layout is None:
            card_layout = self.findChild(QVBoxLayout, "cardLayout")
        if card_layout is not None:
            index = self._tim_vi_tri_form_layout(card_layout)
            card_layout.insertWidget(index + 1 if index >= 0 else 1, list_goi_y)
        return list_goi_y

    def _tim_vi_tri_form_layout(self, layout):
        for index in range(layout.count()):
            item = layout.itemAt(index)
            if item and item.layout() and item.layout().objectName() == "formLayout":
                return index
        return -1

    def _cap_nhat_goi_y(self, text):
        self._list_goi_y.clear()
        tu_khoa = text.strip().upper()
        for xe in self._danh_sach_xe:
            bien_so = xe.get("bien_so", "")
            if tu_khoa and tu_khoa not in bien_so.upper():
                continue
            item = QListWidgetItem(
                f"{bien_so}  |  {xe.get('loai_xe', '')}  |  Vi tri: {xe.get('vi_tri', '')}"
            )
            item.setData(Qt.UserRole, bien_so)
            self._list_goi_y.addItem(item)
        self._list_goi_y.setVisible(self._list_goi_y.count() > 0)

    def _chon_goi_y(self, item):
        self.txt_bien_so.setText(item.data(Qt.UserRole))
        self._list_goi_y.hide()
