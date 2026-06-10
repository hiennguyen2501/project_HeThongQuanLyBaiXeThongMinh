from doituong.phuong_tien import PhuongTien
class ViTriDo:
    def __init__(self, ma_vi_tri, loai_slot):
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
    def xe_dang_do(self):
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
            self._xe_dang_do.xuat()     
        else:
            print("Chưa có xe")   
