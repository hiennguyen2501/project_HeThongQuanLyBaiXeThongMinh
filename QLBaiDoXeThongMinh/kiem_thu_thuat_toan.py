from datetime import datetime, timedelta

from doituong.loai_xe import OTo, XeMay
from dulieu.sap_xep import sap_xep_theo_doanh_thu, sap_xep_theo_thoi_gian_gui
from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe


def in_so_do(bai_xe):
    du_lieu_gui = bai_xe.lay_du_lieu_so_do_cho_gui()
    for hang in du_lieu_gui:
        print([{o["ma_vi_tri"]: o["trang_thai"]} for o in hang])


def kiem_thu_check_in_checkout():
    bai_xe = QuanLyBaiXe(so_hang=2, so_cot=3)
    print("--- KHỞI TẠO BÃI XE THÀNH CÔNG ---")

    gio_vao = datetime.now() - timedelta(hours=2, minutes=10)
    xe1 = XeMay(bien_so="75f1-12345", mau_sac="Đỏ", thoi_gian_vao=gio_vao)
    xe2 = XeMay(bien_so="75F1-67890", mau_sac="Xanh")
    xe3 = XeMay(bien_so="75F1-11111", mau_sac="Trắng")
    xe_cho = XeMay(bien_so="75F1-22222", mau_sac="Đen")
    oto = OTo(bien_so="75A-99999", mau_sac="Bạc", thoi_gian_vao=gio_vao)

    print("\n--- TEST CHECK-IN VỊ TRÍ GẦN CỔNG ---")
    slot1 = bai_xe.check_in_xe(xe1)
    slot2 = bai_xe.check_in_xe(xe2)
    slot3 = bai_xe.check_in_xe(xe3)
    slot_oto = bai_xe.check_in_xe(oto)
    print(f"Xe 1 vào vị trí: {slot1.ma_vi_tri}")
    print(f"Xe 2 vào vị trí: {slot2.ma_vi_tri}")
    print(f"Xe 3 vào vị trí: {slot3.ma_vi_tri}")
    print(f"Ô tô vào vị trí: {slot_oto.ma_vi_tri}")

    print("\n--- TEST HÀNG ĐỢI KHI KHU XE MÁY ĐẦY ---")
    ket_qua_cho = bai_xe.check_in_xe(xe_cho)
    print("Kết quả xe thứ 4:", "Đã vào hàng đợi" if ket_qua_cho is None else ket_qua_cho.ma_vi_tri)
    print("Số xe máy đang chờ:", bai_xe.lay_so_xe_cho_theo_loai("XeMay"))

    print("\n--- DỮ LIỆU ĐẨY RA CHO GUI ---")
    in_so_do(bai_xe)

    print("\n--- TEST CHECK-OUT, TÍNH TIỀN, LƯU LỊCH SỬ ---")
    bien_lai = bai_xe.check_out_va_lap_bien_lai("75F1-12345")
    print(f"Xe xuất bãi: {bien_lai['xe_ra'].bien_so}")
    print(f"Vị trí đã giải phóng/cấp lại: {bien_lai['ma_vi_tri']}")
    print(f"Thành tiền: {bien_lai['tien_gui']:,} đ")
    print("Xe từ hàng đợi vào:", bien_lai["xe_vao_tu_hang_doi"].bien_so)
    print("Số xe máy đang chờ:", bai_xe.lay_so_xe_cho_theo_loai("XeMay"))

    return bai_xe


def kiem_thu_sap_xep():
    du_lieu = [
        {"bien_so": "A", "so_phut_gui": 30, "thanh_tien": 5000},
        {"bien_so": "B", "so_phut_gui": 240, "thanh_tien": 35000},
        {"bien_so": "C", "so_phut_gui": 75, "thanh_tien": 20000},
    ]
    print("\n--- TEST QUICK SORT ---")
    print("Gửi lâu nhất:", [item["bien_so"] for item in sap_xep_theo_thoi_gian_gui(du_lieu)])
    print("Doanh thu cao nhất:", [item["bien_so"] for item in sap_xep_theo_doanh_thu(du_lieu)])


if __name__ == "__main__":
    bai_xe_demo = kiem_thu_check_in_checkout()
    kiem_thu_sap_xep()
    print("\n--- THỐNG KÊ DASHBOARD ---")
    print("Tổng xe đang gửi:", bai_xe_demo.lay_tong_so_xe_dang_gui())
    print("Tỷ lệ lấp đầy:", f"{bai_xe_demo.lay_ty_le_lap_day():.2f}%")
