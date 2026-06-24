from datetime import date, datetime

from doituong.vi_tri_do import ViTriDo
from doituong.loi_ngoai_le import LotFullError, VehicleNotFoundError
from dulieu.sap_xep import sap_xep_theo_doanh_thu, sap_xep_theo_thoi_gian_gui
from dulieu.tep_tin import luu_ban_ghi_lich_su
from xulyhethong.xu_ly_hang_doi import HangDoiXeCho
class QuanLyBaiXe:
    def __init__(self, so_hang=8, so_cot=12):
        self.so_hang = so_hang
        self.so_cot = so_cot
        self.so_do_bai_xe = []
        self.hang_doi = HangDoiXeCho()
        self._lich_su_xe_ra = []
        self.khoi_tao_bai_xe()

    def khoi_tao_bai_xe(self):
        """Khởi tạo mảng động 2 chiều chứa các đối tượng ViTriDo."""
        self.so_do_bai_xe = []
        for r in range(self.so_hang):
            hang_moi = []
            for c in range(self.so_cot):
                loai_slot = "XeMay" if r < self.so_hang // 2 else "OTo"
                khu = chr(ord("A") + r) if loai_slot == "XeMay" else chr(ord("A") + r - self.so_hang // 2)
                ma_vi_tri = f"{khu}{c + 1:02d}"
                hang_moi.append(ViTriDo(ma_vi_tri, loai_slot))
            self.so_do_bai_xe.append(hang_moi)

    def tim_vi_tri_trong_gan_nhat(self, loai_xe):
        """
        Duyệt ma trận từ gần cổng ra xa để tìm ô trống đúng loại xe.
        """
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                if slot.trang_thai == "Trống" and slot.loai_slot == loai_xe:
                    return slot


        raise LotFullError(f"Lỗi: Bãi đỗ xe đã đầy chỗ cho loại xe: {loai_xe}!")


    def check_in_xe(self, phuong_tien, dua_vao_hang_doi=True):
        """
        Xếp xe vào vị trí gần cổng nhất. Nếu hết chỗ, xe được đưa vào hàng đợi.


        Trả về ViTriDo khi có chỗ, trả về None khi xe đã vào hàng đợi.
        """
        if self._bien_so_da_ton_tai(phuong_tien.bien_so):
            raise ValueError(f"Biển số {phuong_tien.bien_so} đang tồn tại trong bãi hoặc hàng đợi")


        try:
            slot_trong = self.tim_vi_tri_trong_gan_nhat(phuong_tien.loai_xe)
        except LotFullError:
            if not dua_vao_hang_doi:
                raise
            self.hang_doi.enqueue(phuong_tien)
            return None


        slot_trong.dat_xe(phuong_tien)
        return slot_trong


    def check_out_xe(self, bien_so):
        """
        API cũ: giải phóng ô đỗ và trả về đối tượng xe để bên ngoài tự tính tiền.
        """
        slot = self._tim_slot_theo_bien_so(bien_so)
        xe_ra = slot.trong_xe()
        self._dua_xe_cho_vao_slot_neu_co(slot)
        return xe_ra


    def check_out_xe_kem_vi_tri(self, bien_so):
        """
        API cũ: giải phóng ô đỗ, trả về xe và mã vị trí.
        """
        slot = self._tim_slot_theo_bien_so(bien_so)
        xe_ra = slot.trong_xe()
        ma_vi_tri = slot.ma_vi_tri
        self._dua_xe_cho_vao_slot_neu_co(slot)
        return xe_ra, ma_vi_tri

    def check_out_va_lap_bien_lai(self, bien_so, thoi_gian_ra=None):
        """
        Checkout đầy đủ: tính tiền, lưu lịch sử, giải phóng ô và tự gọi xe chờ vào.
        """
        thoi_gian_ra = thoi_gian_ra or datetime.now()
        slot = self._tim_slot_theo_bien_so(bien_so)
        xe_ra = slot.trong_xe()
        ma_vi_tri = slot.ma_vi_tri
        tien_gui = xe_ra.tinh_tien_gui(thoi_gian_ra)
        so_phut_gui = max(1, int((thoi_gian_ra - xe_ra.thoi_gian_vao).total_seconds() // 60))
        ban_ghi = {
            "bien_so": xe_ra.bien_so,
            "loai_xe": self._ten_hien_thi_loai_xe(xe_ra.loai_xe),
            "vi_tri": ma_vi_tri,
            "gio_vao": xe_ra.thoi_gian_vao.isoformat(timespec="seconds"),
            "gio_ra": thoi_gian_ra.isoformat(timespec="seconds"),
            "so_phut_gui": so_phut_gui,
            "thanh_tien": tien_gui,
        }
        self._lich_su_xe_ra.append(ban_ghi)
        luu_ban_ghi_lich_su(ban_ghi)
        xe_vao_tu_hang_doi = self._dua_xe_cho_vao_slot_neu_co(slot)


        return {
            "xe_ra": xe_ra,
            "ma_vi_tri": ma_vi_tri,
            "thoi_gian_ra": thoi_gian_ra,
            "so_phut_gui": so_phut_gui,
            "tien_gui": tien_gui,
            "ban_ghi": ban_ghi,
            "xe_vao_tu_hang_doi": xe_vao_tu_hang_doi,
        }


    def _dua_xe_cho_vao_slot_neu_co(self, slot_trong):
        xe_cho = self.hang_doi.dequeue_theo_loai(slot_trong.loai_slot)
        if xe_cho is None:
            return None
        slot_trong.dat_xe(xe_cho)
        return xe_cho


    def _tim_slot_theo_bien_so(self, bien_so):
        bien_so = bien_so.strip().upper()
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                if slot.trang_thai == "Đã có xe" and slot.xe_dang_do.bien_so == bien_so:
                    return slot


        raise VehicleNotFoundError(f"Lỗi: Không tìm thấy phương tiện có biển số {bien_so} trong bãi!")


    def _bien_so_da_ton_tai(self, bien_so):
        try:
            self._tim_slot_theo_bien_so(bien_so)
            return True
        except VehicleNotFoundError:
            pass


        return any(xe.bien_so == bien_so for xe in self.hang_doi.to_list())


    def lay_du_lieu_so_do_cho_gui(self):
        """Chuyển đổi mảng đối tượng thành cấu trúc dữ liệu Dictionary cho GUI đọc."""
        ma_tran_giao_dien = []
        for r in range(self.so_hang):
            hang_gui = []
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                bien_so_xe = slot.xe_dang_do.bien_so if slot.trang_thai == "Đã có xe" else ""
                hang_gui.append({
                    "ma_vi_tri": slot.ma_vi_tri,
                    "loai_slot": slot.loai_slot,
                    "trang_thai": slot.trang_thai,
                    "bien_so": bien_so_xe,
})
            ma_tran_giao_dien.append(hang_gui)
        return ma_tran_giao_dien


    def lay_danh_sach_xe_dang_gui(self):
        danh_sach = []
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                if slot.trang_thai == "Đã có xe":
                    xe = slot.xe_dang_do
                    danh_sach.append({
                        "bien_so": xe.bien_so,
                        "loai_xe": self._ten_hien_thi_loai_xe(xe.loai_xe),
                        "vi_tri": slot.ma_vi_tri,
                        "gio_vao": xe.thoi_gian_vao.strftime("%d/%m/%Y %H:%M"),
                    })
        return danh_sach


    def lay_danh_sach_xe_cho(self):
        return [
            {
                "bien_so": xe.bien_so,
                "loai_xe": self._ten_hien_thi_loai_xe(xe.loai_xe),
                "gio_vao": xe.thoi_gian_vao.strftime("%d/%m/%Y %H:%M"),
            } 
            for xe in self.hang_doi.to_list()
        ]
    def lay_lich_su_xe_ra(self):
        return [self._format_ban_ghi_lich_su(ban_ghi) for ban_ghi in reversed(self._lich_su_xe_ra)]


    def lay_lich_su_gui_lau_nhat(self):
        return [self._format_ban_ghi_lich_su(item) for item in sap_xep_theo_thoi_gian_gui(self._lich_su_xe_ra)]


    def lay_lich_su_doanh_thu_cao_nhat(self):
        return [self._format_ban_ghi_lich_su(item) for item in sap_xep_theo_doanh_thu(self._lich_su_xe_ra)]


    def lay_tong_so_xe_dang_gui(self):
        dem = 0
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                if self.so_do_bai_xe[r][c].trang_thai == "Đã có xe":
                    dem += 1
        return dem


    def lay_so_xe_theo_loai(self, loai_xe):
        dem = 0
        for r in range(self.so_hang):
            for c in range(self.so_cot):
                slot = self.so_do_bai_xe[r][c]
                if slot.loai_slot == loai_xe and slot.trang_thai == "Đã có xe":
                    dem += 1
        return dem


    def lay_so_xe_cho_theo_loai(self, loai_xe):
        return self.hang_doi.dem_theo_loai(loai_xe)


    def lay_tong_so_o(self):
        return self.so_hang * self.so_cot


    def lay_so_o_trong(self):
        return self.lay_tong_so_o() - self.lay_tong_so_xe_dang_gui()


    def lay_du_lieu_theo_loai_slot(self, loai_slot):
        du_lieu = []
        for hang in self.lay_du_lieu_so_do_cho_gui():
            hang_theo_loai = [slot for slot in hang if slot["loai_slot"] == loai_slot]
            if hang_theo_loai:
                du_lieu.append(hang_theo_loai)
        return du_lieu


    def lay_ty_le_lap_day(self):
        tong_so_o = self.lay_tong_so_o()
        if tong_so_o == 0:
            return 0
        return (self.lay_tong_so_xe_dang_gui() / tong_so_o) * 100


    def lay_doanh_thu_theo_ngay(self, ngay=None):
        ngay = ngay or date.today()
        tong_tien = 0
        for ban_ghi in self._lich_su_xe_ra:
            gio_ra = self._parse_datetime(ban_ghi.get("gio_ra"))
            if gio_ra and gio_ra.date() == ngay:
                tong_tien += int(ban_ghi.get("thanh_tien", 0) or 0)
        return tong_tien


    def _format_ban_ghi_lich_su(self, ban_ghi):
        gio_vao = self._parse_datetime(ban_ghi.get("gio_vao"))
        gio_ra = self._parse_datetime(ban_ghi.get("gio_ra"))
        thanh_tien = int(ban_ghi.get("thanh_tien", 0) or 0)
        return {
            "bien_so": ban_ghi.get("bien_so", ""),
            "loai_xe": ban_ghi.get("loai_xe", ""),
            "vi_tri": ban_ghi.get("vi_tri", ""),
            "gio_vao": gio_vao.strftime("%d/%m/%Y %H:%M") if gio_vao else ban_ghi.get("gio_vao", ""),
            "gio_ra": gio_ra.strftime("%d/%m/%Y %H:%M") if gio_ra else ban_ghi.get("gio_ra", ""),
            "so_phut_gui": ban_ghi.get("so_phut_gui", ""),
            "thanh_tien": f"{thanh_tien:,}".replace(",", ".") + " đ",
        }


    def _parse_datetime(self, value):
        if isinstance(value, datetime):
            return value
        if not value:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(str(value), fmt)
            except ValueError:
                continue
        return None


    def _ten_hien_thi_loai_xe(self, loai_xe):
        return "Xe máy" if loai_xe == "XeMay" else "Ô tô"
    



