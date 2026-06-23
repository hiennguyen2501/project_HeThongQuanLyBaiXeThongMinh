
from datetime import datetime
import math
from doituong.phuong_tien import PhuongTien


class XeMay(PhuongTien):
    gia_co_dinh = 5000


    def __init__(self, bien_so, mau_sac="", thoi_gian_vao=None):
        super().__init__(bien_so, loai_xe="XeMay", thoi_gian_vao=thoi_gian_vao)
        self.mau_sac = mau_sac


    def tinh_tien_gui(self, thoi_gian_ra):
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


    def __init__(self, bien_so, mau_sac="", thoi_gian_vao=None):
        super().__init__(bien_so, loai_xe="OTo", thoi_gian_vao=thoi_gian_vao)
        self.mau_sac = mau_sac


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

        
   