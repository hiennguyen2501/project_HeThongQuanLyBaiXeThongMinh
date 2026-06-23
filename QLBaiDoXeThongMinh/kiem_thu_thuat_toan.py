from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe
from xulyhethong.xu_ly_hang_doi import HangDoiXeCho
from doituong.loai_xe import XeMay, OTo
from datetime import datetime

# 1. Khởi tạo bãi xe (2 hàng, mỗi hàng 3 ô)
bai_xe = QuanLyBaiXe(so_hang=2, so_cot=3) 
print("--- KHỞI TẠO BẠI XE THÀNH CÔNG ---")

# 2. Tạo thử 2 xe máy
xe1 = XeMay(bien_so="75F1-12345", mau_sac="Đỏ")
xe2 = XeMay(bien_so="75F1-67890", mau_sac="Xanh")

# 3. Test tính năng Check-in
print("\n--- TEST CHECK-IN ---")
slot1 = bai_xe.check_in_xe(xe1)
print(f"Xe 1 vào vị trí: {slot1.ma_vi_tri} (Loại slot: {slot1.loai_slot})")

slot2 = bai_xe.check_in_xe(xe2)
print(f"Xe 2 vào vị trí: {slot2.ma_vi_tri} (Loại slot: {slot2.loai_slot})")

# 4. Test xuất dữ liệu
print("\n--- DỮ LIỆU ĐẨY RA CHO GUI ---")
du_lieu_gui = bai_xe.lay_du_lieu_so_do_cho_gui()
for hang in du_lieu_gui:
    print([{o['ma_vi_tri']: o['trang_thai']} for o in hang])
    

# 5. Test tính năng Check-out và giải phóng bộ nhớ
print("\n--- TEST CHECK-OUT ---")
xe_ra = bai_xe.check_out_xe("75F1-12345")
print(f"Xe xuất bãi thành công: {xe_ra.bien_so}")
print(f"Trạng thái ô {slot1.ma_vi_tri} sau khi xe ra: {slot1.trang_thai}")
