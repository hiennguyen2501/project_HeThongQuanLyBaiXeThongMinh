from doituong.vi_tri_do import ViTriDo
from doituong.loi_ngoai_le import LotFullError, VehicleNotFoundError

class QuanLyBaiXe:
    def __init__(self, so_hang=5, so_cot=10):
        self.so_hang = so_hang
        self.so_cot = so_cot
        self.so_do_bai_xe = []
        self.khoi_tao_bai_xe()

    def khoi_tao_bai_xe(self):
        """Khởi tạo mảng động 2 chiều chứa các đối tượng ViTriDo"""
        for r in range(self.so_hang):
            hang_moi = []
            for c in range(self.so_cot):
                ma_vi_tri = f"Slot_{r}_{c}"
                # Quy ước: 2 hàng đầu (0 và 1) đỗ XeMay, các hàng còn lại đỗ OTo
                loai_slot = "XeMay" if r < 2 else "OTo"
                
                # Khởi tạo đối tượng ViTriDo
                vi_tri = ViTriDo(ma_vi_tri, loai_slot)
                hang_moi.append(vi_tri)
            self.so_do_bai_xe.append(hang_moi)

    def tim_vi_tri_trong_gan_nhat(self, loai_xe):
        """
        Thuật toán tìm kiếm: Duyệt mảng từ [0][0] (gần cổng nhất) ra xa.
        Trả về đối tượng ViTriDo nếu tìm thấy, ngược lại ném lỗi LotFullError.
        """
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                # Gọi các property của Thành viên 1: .trang_thai và .loai_slot
                if slot.trang_thai == "Trống" and slot.loai_slot == loai_xe:
                    return slot
                    
        raise LotFullError(f"Lỗi: Bãi đỗ xe đã đầy chỗ cho loại xe: {loai_xe}!")

    def check_in_xe(self, phuong_tien):
        """Xử lý xếp xe vào vị trí tối ưu được tìm thấy"""
        # Hàm này sẽ ném ra LotFullError nếu hết chỗ (Thành viên 4 sẽ lấy để đẩy vào Hàng đợi)
        slot_trong = self.tim_vi_tri_trong_gan_nhat(phuong_tien.loai_xe)
        # Sử dụng hàm của Thành viên 1 để gán xe và đổi trạng thái slot
        slot_trong.dat_xe(phuong_tien)
        return slot_trong

    def check_out_xe(self, bien_so):
        """
        Thuật toán tìm kiếm xe theo biển số để xuất bãi.
        Giải phóng bộ nhớ và ô đỗ, trả về đối tượng xe để tính tiền.
        """
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                # Nếu slot có xe và biển số xe khớp với biển số cần tìm
                if slot.trang_thai == "Đã có xe" and slot.xe_dang_do.bien_so == bien_so:
                    xe_ra = slot.xe_dang_do
                    # Sử dụng hàm của Thành viên 1 để giải phóng vị trí (Quản lý bộ nhớ)
                    slot.trong_xe()
                    return xe_ra
                    
        raise VehicleNotFoundError(f"Lỗi: Không tìm thấy phương tiện có biển số {bien_so} trong bãi!")

    # --- HÀM KẾT NỐI DỮ LIỆU ĐỂ THÀNH VIÊN 3 VẼ MÀN HÌNH (GUI) ---
    def lay_du_lieu_so_do_cho_gui(self):
        """Chuyển đổi mảng đối tượng thành cấu trúc dữ liệu Dictionary cho GUI đọc"""
        ma_tran_giao_dien = []
        for r in range(self.so_hang):
            hang_gui = []
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                bien_so_xe = slot.xe_dang_do.bien_so if slot.trang_thai == "Đã có xe" else ""
                
                thong_tin_o = {
                    "ma_vi_tri": slot.ma_vi_tri,
                    "loai_slot": slot.loai_slot,
                    "trang_thai": slot.trang_thai,  # "Trống" hoặc "Đã có xe"
                    "bien_so": bien_so_xe           # Hiển thị khi Thành viên 3 hover chuột
                }
                hang_gui.append(thong_tin_o)
            ma_tran_giao_dien.append(hang_gui)
        return ma_tran_giao_dien

    # --- CÁC HÀM BỔ TRỢ THỐNG KÊ ---
    def lay_tong_so_xe_dang_gui(self):
        dem = 0
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                if self.so_do_bai_xe[r][c].trang_thai == "Đã có xe":
                    dem += 1
        return dem

    def lay_ty_le_lap_day(self):
        tong_so_o = self.so_hang * self.so_cot
        if tong_so_o == 0: return 0
        return (self.lay_tong_so_xe_dang_gui() / tong_so_o) * 100