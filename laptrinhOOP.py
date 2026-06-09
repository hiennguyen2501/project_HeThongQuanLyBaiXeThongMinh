from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import math
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
    def thoi_gian_vao(self, value: datetime):
        self._thoi_gian_vao = value
    def xuat(self):
        print("Biển số:", self._bien_so)
        print("Loại xe:", self._loai_xe)
        print("Thời gian vào:", self._thoi_gian_vao)
    @abstractmethod
    def tinh_tien_gui(self, thoi_gian_ra: datetime) :
       pass
class XeMay(PhuongTien):
    gia_co_dinh = 5000  
    def __init__(self, bien_so: str,mau_sac: str):
        super().__init__(bien_so, loai_xe="XeMay")
        self.mau_sac= mau_sac
    def tinh_tien_gui(self, thoi_gian_ra: datetime) : 
        if thoi_gian_ra < self.thoi_gian_vao:
            return 0
        khoang_thoi_gian = thoi_gian_ra - self.thoi_gian_vao
        so_luot = math.ceil(khoang_thoi_gian.total_seconds() / (24 * 3600))
        return max(1, so_luot) * self.gia_co_dinh
    def xuat(self):
        super().xuat()
        print("Màu sắc:", self.mau_sac)
class OTo(PhuongTien):
    gia_gio_dau = 20000       
    gia_gio_tiep_theo = 15000 
    def __init__(self, bien_so: str, mau_sac:str):
        super().__init__(bien_so, loai_xe="OTo")
        self.mau_sac= mau_sac
    def tinh_tien_gui(self, thoi_gian_ra: datetime) :
        if thoi_gian_ra < self.thoi_gian_vao:
            return 0
        khoang_thoi_gian = thoi_gian_ra - self.thoi_gian_vao
        tong_so_gio = math.ceil(khoang_thoi_gian.total_seconds() / 3600)
        if tong_so_gio <= 1:
            return self.gia_gio_dau
        else:
            return self.gia_gio_dau + (tong_so_gio - 1) * self.gia_gio_tiep_theo
    def xuat(self):
        super().xuat()
        print("Màu sắc:", self.mau_sac)
class ViTriDo:
    def __init__(self, ma_vi_tri: str, loai_slot: str):
        self._ma_vi_tri = ma_vi_tri       
        self._loai_slot = loai_slot        
        self._trang_thai = "Trống"         
        self._xe_dang_do = None            
    @property
    def ma_vi_tri(self):
        return self._ma_vi_tri
    @property
    def loai_slot(self):
        return self._loai_slot
    @property
    def trang_thai(self):
        return self._trang_thai
    @property
    def xe_dang_do(self) -> PhuongTien:
        return self._xe_dang_do
    def dat_xe(self, xe: PhuongTien):
        if self._trang_thai == "Đã có xe":
            print("Vị trí đã có xe")
            return
        if xe.loai_xe != self._loai_slot:
            print("Loại xe không phù hợp vị trí đỗ")
            return
        self._xe_dang_do = xe
        self._trang_thai = "Đã có xe"
    def trong_xe(self):
        self._xe_dang_do = None
        self._trang_thai = "Trống"
    def xuat(self):
        print("Mã vị trí:", self._ma_vi_tri)
        print("Loại vị trí:", self._loai_slot)
        print("Trạng thái:", self._trang_thai)
        if self._xe_dang_do:
            print("Xe đang đỗ:")
            self._xe_dang_do.xuat()
class LotFullError(Exception):
    """Thông báo khi bãi xe không còn vị trí trống cho loại xe tương ứng."""
    def __init__(self, message="Lỗi: Bãi đỗ xe đã đầy!"):
        self.message = message
        super().__init__(self.message)
class VehicleNotFoundError(Exception):
    """Khi nhập biển số xe không có trong bãi."""
    def __init__(self, message="Lỗi: Không tìm thấy phương tiện trong bãi!"):
        self.message = message
        super().__init__(self.message)
