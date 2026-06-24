import sys
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from views.check_in import ICheckinView
from doituong.loai_xe import XeMay, OTo
from doituong.loi_ngoai_le import LotFullError

class CheckInPresenter:
    def __init__(self, view: ICheckinView, bai_xe=None, callback_cap_nhat=None):
        self._view = view
        self._bai_xe = bai_xe
        self._callback_cap_nhat = callback_cap_nhat
        self._view.yeu_cau_xac_nhan.connect(self.xu_ly_check_in)

    def xu_ly_check_in(self):
        bien_so = self._view.lay_bien_so().strip()
        if not bien_so:
           self._view.bao_loi("Vui lòng nhập biển số xe")

        loai_xe_text = self._view.lay_loai_xe()

        if self._bai_xe is None:
            self._view.bao_loi("Hệ thống bãi xe chưa được khởi tạo")
            return

        try:
            if loai_xe_text == "Xe máy":
                xe = XeMay(bien_so)
            else:
                xe = OTo(bien_so)

            vi_tri = self._bai_xe.check_in_xe(xe)

            if vi_tri is None:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self._view,
                    "Hàng đợi",
                    f"Bãi đã đầy. Xe {bien_so} đã được đưa vào hàng đợi.",
                )
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self._view,
                    "Thành công",
                    f"Xe {bien_so} đã được xếp vào vị trí {vi_tri.ma_vi_tri}.",
                )

        except ValueError as e:
            self._view.bao_loi(str(e))
            return
        except LotFullError as e:
            self._view.bao_loi(str(e))
            return

        if self._callback_cap_nhat:
            self._callback_cap_nhat()
        self._view.dong_thanh_cong()