from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class SoDoBaiXe(QDialog):
    def __init__(self):
        super().__init__()
        # Giả sử bạn đã load giao diện ui từ Qt Designer vào thành công
        # self.ui.setupUi(self)
        
        # Thiết lập Layout Lưới cho vùng chứa sơ đồ trên Tab Tầng B1
        # (Thay 'widget_so_do' bằng objectName của Widget bạn đặt trên Designer)
        self.grid_layout = QGridLayout(self.ui.widget_so_do)
        self.grid_layout.setSpacing(6) # Khoảng cách giữa các ô xe
        
        # Giả lập danh sách các vị trí đã có xe (True = Đã có xe/Màu đỏ, False = Trống/Màu xanh)
        # Trong thực tế, mảng này bạn sẽ lấy về từ Cơ sở dữ liệu (Database)
        self.trang_thai_bai_xe = {
            "A01": True, "A02": True, "A03": True, "A23": False, "A24": False,
            "B01": True, "B02": True, "B08": False, "B17": True, "B24": True
            # ... bạn khai báo tiếp hoặc dùng vòng lặp để gán tự động
        }
        
        self.khoi_tao_so_do()

    def khoi_tao_so_do(self):
        # Tạo danh sách các hàng A và B, mỗi hàng có 24 vị trí chia thành các cụm
        for row_idx, khu in enumerate(["A", "B"]):
            for num in range(1, 25):
                ten_vi_tri = f"{khu}{num:02d}" # Kết quả: A01, A02...
                
                # 1. Tạo nút bấm cho từng ô đỗ
                btn = QPushButton(ten_vi_tri)
                btn.setProperty("class", "SlotBtn") # Ăn theo định dạng CSS ở Bước 3
                
                # 2. Xoay dọc chữ bằng cách tận dụng hiệu ứng Layout (Tùy chọn)
                # Hoặc viết chữ kiểu xuống dòng: "A\n0\n1" để chữ tự dọc thẳng như ảnh mẫu
                btn.setText("\n".join(list(ten_vi_tri)))
                
                # 3. Kiểm tra trạng thái để nhuộm màu Đỏ / Xanh cho nút
                da_co_xe = self.trang_thai_bai_xe.get(ten_vi_tri, True) # Mặc định nếu thiếu gán là Có xe (Đỏ)
                if da_co_xe:
                    btn.setStyleSheet("background-color: #FF3D00; color: #000000;") # Màu đỏ
                else:
                    btn.setStyleSheet("background-color: #00C853; color: #000000;") # Màu xanh lá
                
                # 4. Tính toán vị trí Tọa độ (Hàng, Cột) trong Grid Layout để tạo khe lối đi ở giữa
                # Căn cứ theo ảnh: Cứ 2 cột xe sát nhau thì có 1 khoảng trống nhỏ
                col_offset = (num - 1) // 2
                vi_tri_cot = (num - 1) * 2 + col_offset
                
                # Định vị vị trí hàng: Hàng A nằm cụm trên, hàng B nằm cụm dưới
                vi_tri_hang = row_idx * 4 if num <= 12 else row_idx * 4 + 1
                if num > 12:
                    vi_tri_cot = (num - 13) * 2 + ((num - 13) // 2)
                    vi_tri_hang = row_idx * 4 + 2 # Đẩy xuống cụm dưới
                
                # 5. Add nút vào lưới tự động
                self.grid_layout.addWidget(btn, vi_tri_hang, vi_tri_cot)
                
                # 6. Bắt sự kiện khi thủ kho bấm vào ô đỗ xe bất kỳ để xem thông tin
                btn.clicked.connect(lambda checked, vt=ten_vi_tri: self.click_o_do_xe(vt))

    def click_o_do_xe(self, vi_tri):
        print(f"Bạn vừa click vào vị trí đỗ xe: {vi_tri}")
        # Tại đây bạn có thể mở Form "Thống kê chi tiết" hoặc Form Check-out ra!