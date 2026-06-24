import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from doituong.loai_xe import OTo, XeMay
from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe


class ParkingService:
    """Service/Model: gom nghiep vu bai xe, an chi tiet QuanLyBaiXe khoi Presenter."""

    def __init__(self, bai_xe=None):
        self._bai_xe = bai_xe or QuanLyBaiXe()

    def check_in(self, bien_so, loai_xe_hien_thi):
        xe = XeMay(bien_so) if loai_xe_hien_thi == "Xe may" or loai_xe_hien_thi == "Xe máy" else OTo(bien_so)
        vi_tri = self._bai_xe.check_in_xe(xe)
        return {
            "vao_hang_doi": vi_tri is None,
            "bien_so": bien_so,
            "ma_vi_tri": None if vi_tri is None else vi_tri.ma_vi_tri,
        }

    def check_out(self, bien_so):
        return self._bai_xe.check_out_va_lap_bien_lai(bien_so)

    def lay_dashboard(self):
        so_xe_dang_gui = self._bai_xe.lay_tong_so_xe_dang_gui()
        tong_so_o = self._bai_xe.lay_tong_so_o()
        return {
            "xe_may": self._bai_xe.lay_so_xe_theo_loai("XeMay"),
            "oto": self._bai_xe.lay_so_xe_theo_loai("OTo"),
            "doanh_thu": self._bai_xe.lay_doanh_thu_theo_ngay(),
            "xe_may_cho": self._bai_xe.lay_so_xe_cho_theo_loai("XeMay"),
            "oto_cho": self._bai_xe.lay_so_xe_cho_theo_loai("OTo"),
            "so_xe_dang_gui": so_xe_dang_gui,
            "tong_so_o": tong_so_o,
            "ty_le_lap_day": self._bai_xe.lay_ty_le_lap_day(),
        }

    def lay_danh_sach_xe_dang_gui(self):
        return self._bai_xe.lay_danh_sach_xe_dang_gui()

    def lay_lich_su_xe_ra(self):
        return self._bai_xe.lay_lich_su_xe_ra()

    def lay_so_do_xe_may(self):
        return self._bai_xe.lay_du_lieu_theo_loai_slot("XeMay")

    def lay_so_do_oto(self):
        return self._bai_xe.lay_du_lieu_theo_loai_slot("OTo")

    def lay_lich_su_doanh_thu_cao_nhat(self):
        return self._bai_xe.lay_lich_su_doanh_thu_cao_nhat()

    def lay_lich_su_gui_lau_nhat(self):
        return self._bai_xe.lay_lich_su_gui_lau_nhat()
