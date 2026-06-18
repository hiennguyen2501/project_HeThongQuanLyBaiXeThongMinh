from views.check_in import ICheckinView
import os
import sys


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from doituong.loai_xe import XeMay, OTo

class CheckInPresenter:
    def __init__(self, view:ICheckinView, bai_xe=None, on_success=None):
        self._view = view
        self._bai_xe = bai_xe
        self._on_success = on_success
        self._view.yeu_cau_xac_nhan.connect(self.xu_ly_check_in)

    def xu_ly_check_in(self):
        bien_so = self._view.lay_bien_so().strip()
        if not bien_so:
            self._view.bao_loi("Vui Long Nhap Bien So")
            return
        
        loai_xe = self._view.lay_loai_xe()
        if self._bai_xe is not None:
            try:
                phuong_tien = XeMay(bien_so, "") if loai_xe == "Xe máy" else OTo(bien_so, "")
                slot = self._bai_xe.check_in_xe(phuong_tien)
            except Exception as error:
                self._view.bao_loi(str(error))
                return
            if hasattr(self._view, "bao_thong_tin"):
                if slot is None:
                    self._view.bao_thong_tin("Bãi đã đầy, xe đã được đưa vào hàng đợi")
                else:
                    self._view.bao_thong_tin(f"Đã xếp xe vào vị trí {slot.ma_vi_tri}")

        if self._on_success:
            self._on_success()
        self._view.dong_thanh_cong()
