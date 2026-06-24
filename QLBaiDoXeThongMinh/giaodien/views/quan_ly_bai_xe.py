from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QStyle, QTableWidgetItem
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "..", "designer", "quan_ly_bai_xe.ui")


class QuanLyBaiXeWindow(QMainWindow):
    yeu_cau_xuat_thong_ke = pyqtSignal()

    def __init__(self, tab_index=0):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.tabWidget.setCurrentIndex(tab_index)
        self.btn_xuat_excel.setText("Thống kê")
        self.btn_xuat_excel.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.btn_xuat_excel.setVisible(tab_index == 1)
        self.btn_xuat_excel.clicked.connect(self.yeu_cau_xuat_thong_ke.emit)
        self.tabWidget.currentChanged.connect(self._cap_nhat_nut_thong_ke)

    def hien_du_lieu(self, xe_dang_gui, lich_su_xe_ra):
        self._do_du_lieu_bang(
            self.tableWidget,
            xe_dang_gui,
            ["bien_so", "loai_xe", "vi_tri", "gio_vao", "hanh_dong"],
            {"hanh_dong": "ĐANG GỬI"},
        )
        self._do_du_lieu_bang(
            self.tableWidget_2,
            lich_su_xe_ra,
            ["bien_so", "loai_xe", "vi_tri", "gio_vao", "gio_ra", "thanh_tien"],
        )

    def _cap_nhat_nut_thong_ke(self, index):
        self.btn_xuat_excel.setVisible(index == 1)

    def _do_du_lieu_bang(self, table, rows, columns, gia_tri_mac_dinh=None):
        gia_tri_mac_dinh = gia_tri_mac_dinh or {}
        table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, column in enumerate(columns):
                value = row_data.get(column, gia_tri_mac_dinh.get(column, ""))
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
