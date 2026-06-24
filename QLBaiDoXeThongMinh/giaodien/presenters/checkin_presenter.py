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
            self._view.bao_loi("Vui long nhap bien so xe")
            return

        if self._parking_service is None:
            self._view.bao_loi("He thong bai xe chua duoc khoi tao")
            return

        try:
            ket_qua = self._parking_service.check_in(bien_so, self._view.lay_loai_xe())
        except (ValueError, LotFullError) as error:
            self._view.bao_loi(str(error))
            return

        if ket_qua["vao_hang_doi"]:
            self._view.thong_bao("Hang doi", f"Bai da day. Xe {bien_so} da duoc dua vao hang doi.")
        else:
            self._view.thong_bao("Thanh cong", f"Xe {bien_so} da duoc xep vao vi tri {ket_qua['ma_vi_tri']}.")

        if self._callback_cap_nhat:
            self._callback_cap_nhat()
        self._view.dong_thanh_cong()
