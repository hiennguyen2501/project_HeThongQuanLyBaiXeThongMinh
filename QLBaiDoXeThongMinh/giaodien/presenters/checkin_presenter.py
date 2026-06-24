import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from doituong.loi_ngoai_le import LotFullError
from views.check_in import ICheckinView


class CheckInPresenter:
    def __init__(self, view: ICheckinView, parking_service=None, callback_cap_nhat=None):
        self._view = view
        self._parking_service = parking_service
        self._callback_cap_nhat = callback_cap_nhat
        self._view.yeu_cau_xac_nhan.connect(self.xu_ly_check_in)

    def xu_ly_check_in(self):
        bien_so = self._view.lay_bien_so().strip().upper()
        if not bien_so:
            self._view.bao_loi("Vui lòng nhập biển số xe")
            return

        if self._parking_service is None:
            self._view.bao_loi("Hệ thống bãi xe chưa được khởi tạo")
            return

        try:
            ket_qua = self._parking_service.check_in(bien_so, self._view.lay_loai_xe())
        except (ValueError, LotFullError) as error:
            self._view.bao_loi(str(error))
            return

        if ket_qua["vao_hang_doi"]:
            self._view.thong_bao(
                "Hàng đợi",
                f"Bãi đã đầy. Xe {bien_so} đã được thêm vào danh sách xe chờ.",
            )
        else:
            self._view.thong_bao(
                "Check-in thành công",
                f"Xe {bien_so} đã được thêm vào danh sách xe đang gửi tại vị trí {ket_qua['ma_vi_tri']}.",
            )

        if self._callback_cap_nhat:
            self._callback_cap_nhat()
        self._view.dong_thanh_cong()
