from datetime import datetime

xe_dang_do = {}

def check_in(bien_so):
    # 1. Ghi lại thời gian vào
    thoi_gian_vao = datetime.now()
    xe_dang_do[bien_so] = thoi_gian_vao
    print(f"Xe {bien_so} đã vào bãi lúc: {thoi_gian_vao.strftime('%H:%M:%S')}")
    # TODO: Gọi hàm của Thành viên 3 để cập nhật GUI (đổi màu đỏ)

def check_out(bien_so, don_gia_moi_gio=10000):
    if bien_so in xe_dang_do:
        # 1. Lấy thời gian vào và thời gian hiện tại
        thoi_gian_vao = xe_dang_do[bien_so]
        thoi_gian_ra = datetime.now()
        
        # 2. Tính khoảng cách (delta)
        delta = thoi_gian_ra - thoi_gian_vao
        gio_do = delta.total_seconds() / 3600
        
        # 3. Tính tiền
        tien_phai_tra = gio_do * don_gia_moi_gio
        
        print(f"Xe {bien_so} ra. Đã đỗ {gio_do:.2f} giờ. Tổng tiền: {tien_phai_tra:.0f} VND")
        
        # 4. Xóa khỏi "Bộ nhớ" (Giải phóng RAM)
        del xe_dang_do[bien_so]
        # TODO: Gọi hàm của Thành viên 3 để cập nhật GUI (đổi màu xanh)
    else:
        print("Không tìm thấy xe này trong bãi!")

# --- THỬ NGHIỆM ---
check_in("75A-12345")
# (Giả sử xe đỗ một lúc...)
check_out("75A-12345")