"""Presenter tang trang chu: dieu phoi View va Service theo mo hinh MVP."""
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from doituong.loi_ngoai_le import LotFullError, VehicleNotFoundError
from presenters.checkin_presenter import CheckInPresenter
from services.hoa_don_service import HoaDonService
from services.parking_service import ParkingService
from services.thong_ke_service import ThongKeService
from views.check_in import CheckInDialog
from views.check_out import CheckOutDialog
from views.quan_ly_bai_xe import QuanLyBaiXeWindow
from views.so_do import SoDoBaiXeWindow
from views.thong_tin_xe_ra import ThongTinXeRaDialog
from views.trang_chu import ITrangChuView


class TrangChuPresenter:
    def __init__(self, view: ITrangChuView, parking_service=None):
        self._view = view
        self._parking_service = parking_service or ParkingService()
        self._hoa_don_service = HoaDonService()
        self._thong_ke_service = ThongKeService()
        self._windows = []
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
        dialog._presenter = CheckInPresenter(dialog, self._parking_service, self._cap_nhat_dashboard)
        dialog.exec_()

    def mo_man_hinh_check_out(self):
        dialog = CheckOutDialog()
        dialog.hien_danh_sach_goi_y(self._parking_service.lay_danh_sach_xe_dang_gui())
        dialog.yeu_cau_xac_nhan.connect(lambda: self._xu_ly_check_out(dialog))
        dialog.exec_()

    def mo_man_hinh_quan_ly_bai_xe(self):
        self._mo_man_hinh_quan_ly(tab_index=0)

    def mo_man_hinh_thong_ke_chi_tiet(self):
        self._mo_man_hinh_quan_ly(tab_index=1)

    def mo_man_hinh_so_do(self, tang=0):
        window = SoDoBaiXeWindow(tang)
        window.hien_so_do(
            self._parking_service.lay_so_do_xe_may(),
            self._parking_service.lay_so_do_oto(),
        )
        window.show()
        self._windows.append(window)

    def _mo_man_hinh_quan_ly(self, tab_index=0):
        window = QuanLyBaiXeWindow(tab_index)
        window.yeu_cau_xuat_thong_ke.connect(lambda: self._xuat_excel_thong_ke(window))
        self._cap_nhat_bang_quan_ly(window)
        window.show()
        self._windows.append(window)

    def _xu_ly_check_out(self, dialog):
        bien_so = dialog.lay_bien_so()
        if not bien_so:
            dialog.bao_loi("Vui lòng nhập biển số xe cần check-out")
            return

        try:
            bien_lai = self._parking_service.check_out(bien_so)
        except VehicleNotFoundError as error:
            dialog.bao_loi(str(error))
            return

        self._cap_nhat_dashboard()
        dialog.dong_thanh_cong()
        QMessageBox.information(
            self._view,
            "Check-out thành công",
            f"Xe {bien_lai['xe_ra'].bien_so} đã rời bãi đỗ xe"
        )
        self._mo_thong_tin_xe_ra(bien_lai)

    def _mo_thong_tin_xe_ra(self, bien_lai):
        dialog = ThongTinXeRaDialog(bien_lai)
        dialog.yeu_cau_xuat_hoa_don.connect(lambda file_path: self._xuat_anh_hoa_don(dialog, bien_lai, file_path))
        dialog.exec_()

    def _xuat_anh_hoa_don(self, dialog, bien_lai, file_path):
        if self._hoa_don_service.xuat_anh_hoa_don(bien_lai, file_path):
            dialog.thong_bao("Thành công", f"Đã xuất ảnh hóa đơn:\n{file_path}")
        else:
            dialog.bao_loi("Không thể lưu ảnh hóa đơn.")

    def _xuat_excel_thong_ke(self, parent):
        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Lưu file thống kê",
            "thong_ke_bai_xe.xlsx",
            "Excel Files (*.xlsx)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".xlsx"):
            file_path += ".xlsx"

        try:
            self._thong_ke_service.xuat_excel(
                file_path,
                self._parking_service.lay_lich_su_doanh_thu_cao_nhat(),
                self._parking_service.lay_lich_su_gui_lau_nhat(),
            )
        except ImportError:
            QMessageBox.warning(parent, "Thiếu thư viện", "Cần cài đặt openpyxl để xuất Excel.")
            return
        except Exception as error:
            QMessageBox.warning(parent, "Lỗi", f"Không thể lưu file:\n{error}")
            return
        QMessageBox.information(parent, "Thành công", f"Đã xuất Excel:\n{file_path}")

    def _cap_nhat_dashboard(self):
        data = self._parking_service.lay_dashboard()
        self._view.hien_so_xe(data["xe_may"], data["oto"])
        self._view.hien_doanh_thu(data["doanh_thu"])
        self._view.hien_xe_cho(data["xe_may_cho"], data["oto_cho"])
        if hasattr(self._view, "hien_ty_le_lap_day"):
            self._view.hien_ty_le_lap_day(
                data["so_xe_dang_gui"],
                data["tong_so_o"],
                data["ty_le_lap_day"],
            )
        self._cap_nhat_cac_bang_quan_ly()

    def _cap_nhat_cac_bang_quan_ly(self):
        for window in self._windows:
            if isinstance(window, QuanLyBaiXeWindow):
                self._cap_nhat_bang_quan_ly(window)

    def _cap_nhat_bang_quan_ly(self, window):
        window.hien_du_lieu(
            self._parking_service.lay_danh_sach_xe_dang_gui(),
            self._parking_service.lay_lich_su_xe_ra(),
        )

