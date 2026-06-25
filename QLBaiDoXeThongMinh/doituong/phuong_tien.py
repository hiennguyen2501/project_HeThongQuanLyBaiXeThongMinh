from abc import ABC, abstractmethod
from datetime import datetime
import re


BIEN_SO_REGEX = re.compile(
    r"^\d{2}[A-Z]\d?[-\s]?\d{3,5}\.?\d{0,2}$"
)


def kiem_tra_bien_so(bien_so: str) -> bool:
    return bool(BIEN_SO_REGEX.match(bien_so))


class PhuongTien(ABC):
    def __init__(self, bien_so: str, loai_xe: str, thoi_gian_vao: datetime = None):
        bien_so = bien_so.strip().upper()
        if not bien_so:
            raise ValueError("Biển số xe không được để trống")
        if not kiem_tra_bien_so(bien_so):
            raise ValueError(
                f"Biển số '{bien_so}' không đúng quy định.\n"
                "Định dạng hợp lệ: 38A-12345, 51F-123.45, 30A1-12345"
            )
        self._bien_so = bien_so
        self._loai_xe = loai_xe
        self._thoi_gian_vao = thoi_gian_vao or datetime.now()


    @property
    def bien_so(self):
        return self._bien_so


    @property
    def loai_xe(self):
        return self._loai_xe


    @property
    def thoi_gian_vao(self):
        return self._thoi_gian_vao


    @thoi_gian_vao.setter
    def thoi_gian_vao(self, value):
        if not isinstance(value, datetime):
            raise TypeError("Thời gian vào phải là datetime")
        self._thoi_gian_vao = value


    def xuat(self):
        print("Biển số:", self._bien_so)
        print("Loại xe:", self._loai_xe)
        print("Thời gian vào:", self._thoi_gian_vao)


    @abstractmethod
    def tinh_tien_gui(self, thoi_gian_ra):
        pass
