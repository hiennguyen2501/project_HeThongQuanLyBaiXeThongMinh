from abc import ABC, abstractmethod
from datetime import datetime
class PhuongTien(ABC):
    def __init__(self, bien_so: str, loai_xe: str):
        self._bien_so = bien_so
        self._loai_xe = loai_xe
        self._thoi_gian_vao = datetime.now()
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
        self._thoi_gian_vao = value
    def xuat(self):
        print("Biển số:", self._bien_so)
        print("Loại xe:", self._loai_xe)
        print("Thời gian vào:", self._thoi_gian_vao)
    @abstractmethod
    def tinh_tien_gui(self, thoi_gian_ra):
        pass