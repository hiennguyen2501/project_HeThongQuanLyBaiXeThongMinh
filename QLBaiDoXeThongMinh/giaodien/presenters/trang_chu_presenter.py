"""
Tầng Presenter
Cầu nối: Lấy dữ liệu từ Service -> đẩy vào View: Nhận signal từ view -> xử lý
nguyên tắc là View và Service không biết gì nhau

"""
from views.trang_chu import ITrangChuView
from views.check_in import CheckInDialog
from presenters.checkin_presenter import CheckInPresenter
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QPushButton, QTableWidgetItem
import os
import sys


DESIGNER_DIR = os.path.join(os.path.dirname(__file__), "..", "designer")
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe
from doituong.loi_ngoai_le import VehicleNotFoundError


class TrangChuPresenter: 
    def __init__(self, view:ITrangChuView):
        self._view = view
        self._windows = []
        self._bai_xe = QuanLyBaiXe()
        self._noi_su_kien()

    def _noi_su_kien(self):
        self._view.yeu_cau_checkin.connect(self.mo_man_hinh_check_in)
        self._view.yeu_cau_checkout.connect(self.mo_man_hinh_check_out)
        self._view.yeu_cau_quan_ly_bai_xe.connect(self.mo_man_hinh_quan_ly_bai_xe)
        self._view.yeu_cau_thong_ke_chi_tiet.connect(self.mo_man_hinh_thong_ke_chi_tiet)
        self._view.yeu_cau_so_do.connect(self.mo_man_hinh_so_do)

    def load(self):
        self._cap_nhat_dashboard()

    def mo_man_hinh_check_in(self):
        dialog = CheckInDialog()
        presenter = CheckInPresenter(dialog, self._bai_xe, self._cap_nhat_dashboard)
        dialog.exec_()

    def mo_man_hinh_check_out(self):
        dialog = self._load_dialog("check_out.ui")
        if hasattr(dialog, "btn_checkout"):
            dialog.btn_checkout.clicked.connect(lambda: self._xu_ly_check_out(dialog))
        dialog.exec_()

    def mo_man_hinh_quan_ly_bai_xe(self):
        self._mo_man_hinh_quan_ly(tab_index=0)

    def _mo_man_hinh_quan_ly(self, tab_index=0):
        window = QMainWindow()
        uic.loadUi(os.path.join(DESIGNER_DIR, "quan_ly_bai_xe.ui"), window)
        self._cap_nhat_bang_quan_ly(window)
        if hasattr(window, "tabWidget"):
            window.tabWidget.setCurrentIndex(tab_index)
        window.show()
        self._windows.append(window)

    def mo_man_hinh_so_do(self, tang=0):
        window = QMainWindow()
        uic.loadUi(os.path.join(DESIGNER_DIR, "so_do.ui"), window)
        self._khoi_tao_so_do(window)
        window.tabWidget.setCurrentIndex(tang)
        window.show()
        self._windows.append(window)

    def mo_man_hinh_thong_ke_chi_tiet(self):
        self._mo_man_hinh_quan_ly(tab_index=1)

    def mo_man_hinh_thong_tin_xe_ra(self):
        dialog = self._load_dialog("thong_tin_xe_ra.ui")
        dialog.exec_()

    def _load_dialog(self, ui_file):
        dialog = QDialog()
        uic.loadUi(os.path.join(DESIGNER_DIR, ui_file), dialog)
        return dialog

    def _khoi_tao_so_do(self, window):
        self._ve_tang(window, window.gridLayout, self._bai_xe.lay_du_lieu_theo_loai_slot("XeMay"))
        self._ve_tang(window, window.gridLayout_2, self._bai_xe.lay_du_lieu_theo_loai_slot("OTo"))

    def _ve_tang(self, window, layout, du_lieu_tang):
        for row_group, hang_slot in enumerate(du_lieu_tang):
            for index, slot in enumerate(hang_slot):
                button = self._tao_nut_vi_tri(window, slot)
                hang = row_group
                cot = index + index // 2
                layout.addWidget(button, hang, cot)

    def _tao_nut_vi_tri(self, window, slot):
        ma_vi_tri = slot["ma_vi_tri"]
        con_trong = slot["trang_thai"] == "Trống"
        button = QPushButton("\n".join(ma_vi_tri))
        button.setProperty("class", "SlotBtn")
        button.setMinimumSize(58, 72)
        button.setStyleSheet(
            "background-color: #09C56B; color: #050505; border-radius: 8px; font-weight: 900;"
            if con_trong
            else "background-color: #FF3238; color: #050505; border-radius: 8px; font-weight: 900;"
        )
        trang_thai = "Còn trống" if con_trong else f"Đã có xe\nBiển số: {slot['bien_so']}"
        button.clicked.connect(
            lambda checked=False, vt=ma_vi_tri, tt=trang_thai: QMessageBox.information(
                window,
                "Thông tin vị trí",
                f"Vị trí {vt}: {tt}",
            )
        )
        return button

    def _cap_nhat_dashboard(self):
        self._view.hien_so_xe(
            self._bai_xe.lay_so_xe_theo_loai("XeMay"),
            self._bai_xe.lay_so_xe_theo_loai("OTo"),
        )
        self._view.hien_doanh_thu(self._bai_xe.lay_doanh_thu_theo_ngay())
        self._view.hien_xe_cho(
            self._bai_xe.lay_so_xe_cho_theo_loai("XeMay"),
            self._bai_xe.lay_so_xe_cho_theo_loai("OTo"),
        )
        if hasattr(self._view, "hien_ty_le_lap_day"):
            self._view.hien_ty_le_lap_day(
                self._bai_xe.lay_tong_so_xe_dang_gui(),
                self._bai_xe.lay_tong_so_o(),
                self._bai_xe.lay_ty_le_lap_day(),
            )
        self._cap_nhat_cac_bang_quan_ly()

    def _xu_ly_check_out(self, dialog):
        bien_so = dialog.txt_bien_so.text().strip() if hasattr(dialog, "txt_bien_so") else ""
        if not bien_so:
            QMessageBox.warning(dialog, "Lỗi", "Vui lòng nhập biển số xe")
            return

        try:
            bien_lai = self._bai_xe.check_out_va_lap_bien_lai(bien_so)
        except VehicleNotFoundError as error:
            QMessageBox.warning(dialog, "Lỗi", str(error))
            return

        self._cap_nhat_dashboard()
        dialog.accept()
        self._mo_thong_tin_xe_ra(bien_lai)

    def _mo_thong_tin_xe_ra(self, bien_lai):
        xe_ra = bien_lai["xe_ra"]
        ma_vi_tri = bien_lai["ma_vi_tri"]
        thoi_gian_ra = bien_lai["thoi_gian_ra"]
        tien_gui = bien_lai["tien_gui"]
        dialog = self._load_dialog("thong_tin_xe_ra.ui")
        if hasattr(dialog, "lbl_bien_so"):
            dialog.lbl_bien_so.setText(xe_ra.bien_so)
        if hasattr(dialog, "lbl_loai_xe"):
            dialog.lbl_loai_xe.setText("Xe máy" if xe_ra.loai_xe == "XeMay" else "Ô tô")
        if hasattr(dialog, "lbl_vi_tri_do"):
            dialog.lbl_vi_tri_do.setText(ma_vi_tri)
        if hasattr(dialog, "lbl_gio_vao"):
            dialog.lbl_gio_vao.setText(xe_ra.thoi_gian_vao.strftime("%d/%m/%Y %H:%M"))
        if hasattr(dialog, "lbl_gio_ra"):
            dialog.lbl_gio_ra.setText(thoi_gian_ra.strftime("%d/%m/%Y %H:%M"))
        if hasattr(dialog, "lbl_thoi_gian_gui"):
            so_phut = int(bien_lai["so_phut_gui"])
            dialog.lbl_thoi_gian_gui.setText(f"{so_phut // 60} giờ {so_phut % 60} phút")
        if hasattr(dialog, "lbl_thanh_tien"):
            dialog.lbl_thanh_tien.setText(f"{tien_gui:,}".replace(",", ".") + " đ")
        xe_cho = bien_lai.get("xe_vao_tu_hang_doi")
        if xe_cho is not None:
            QMessageBox.information(
                dialog,
                "Hàng đợi",
                f"Xe {xe_cho.bien_so} đã được tự động xếp vào vị trí {ma_vi_tri}.",
            )
        dialog.exec_()

    def _cap_nhat_cac_bang_quan_ly(self):
        for window in self._windows:
            if hasattr(window, "tableWidget") and hasattr(window, "tableWidget_2"):
                self._cap_nhat_bang_quan_ly(window)

    def _cap_nhat_bang_quan_ly(self, window):
        self._do_du_lieu_bang(
            window.tableWidget,
            self._bai_xe.lay_danh_sach_xe_dang_gui(),
            ["bien_so", "loai_xe", "vi_tri", "gio_vao", "hanh_dong"],
            gia_tri_mac_dinh={"hanh_dong": "CHECK-OUT"},
        )
        self._do_du_lieu_bang(
            window.tableWidget_2,
            self._bai_xe.lay_lich_su_xe_ra(),
            ["bien_so", "loai_xe", "vi_tri", "gio_vao", "gio_ra", "thanh_tien"],
        )

    def _do_du_lieu_bang(self, table, rows, columns, gia_tri_mac_dinh=None):
        gia_tri_mac_dinh = gia_tri_mac_dinh or {}
        table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, column in enumerate(columns):
                value = row_data.get(column, gia_tri_mac_dinh.get(column, ""))
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
