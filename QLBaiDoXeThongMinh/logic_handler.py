class XeService:
    def __init__(self):
        self.danh_sach_xe_trong_bai = {}
        self.don_gia_xe_may = 5000
        self.don_gia_oto = 20000

    def xu_ly_check_in(self, bien_so, loai_xe):
        self.danh_sach_xe_trong_bai[bien_so] = loai_xe
        return f"Xe {bien_so} đã vào bãi."

    def xu_ly_check_out(self, bien_so):
        if bien_so not in self.danh_sach_xe_trong_bai:
            return "Xe không có trong bãi!"
    #Tính tiền
        tien_thanh_toan = self.don_gia_xe_may
        print(f"Xe {bien_so} ra.Tổng tiền: {tien_thanh_toan:.0f} VND")
    #Giải phóng chỗ
        del self.danh_sach_xe_trong_bai[bien_so]
        return {"tiền": tien_thanh_toan, "trạng thái": " Đã thanh toán"}
    