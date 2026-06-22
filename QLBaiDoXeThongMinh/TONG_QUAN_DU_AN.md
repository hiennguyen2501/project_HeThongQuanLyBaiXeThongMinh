# TỔNG QUAN DỰ ÁN HỆ THỐNG QUẢN LÝ BÃI XE THÔNG MINH

## 1. Giới thiệu dự án

`QLBaiDoXeThongMinh` là một ứng dụng quản lý bãi đỗ xe được xây dựng bằng Python và PyQt5. Dự án mô phỏng quy trình vận hành của một bãi xe thông minh, bao gồm tiếp nhận xe vào bãi, sắp xếp vị trí đỗ phù hợp, xử lý xe ra bãi, tính tiền gửi xe, quản lý hàng đợi khi bãi đầy, lưu lịch sử giao dịch và hiển thị các thông tin thống kê trên giao diện đồ họa.

Ứng dụng được thiết kế theo hướng tách lớp tương đối rõ ràng:

- Lớp đối tượng nghiệp vụ nằm trong thư mục `doituong`.
- Lớp xử lý hệ thống nằm trong thư mục `xulyhethong`.
- Lớp lưu trữ và thuật toán dữ liệu nằm trong thư mục `dulieu`.
- Lớp giao diện và điều phối giao diện nằm trong thư mục `giaodien`.

Mục tiêu chính của dự án là giúp người dùng quản lý trạng thái bãi xe theo thời gian thực, thao tác check-in/check-out nhanh, tự động tính phí gửi xe và có dữ liệu lịch sử phục vụ thống kê.

## 2. Công nghệ sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Ngôn ngữ lập trình | Python |
| Giao diện người dùng | PyQt5 |
| Thiết kế giao diện | Qt Designer, file `.ui` |
| Lưu trữ dữ liệu | CSV và JSON |
| Kiến trúc giao diện | Gần với mô hình MVP: View - Presenter - Service/Model |
| Cấu trúc dữ liệu nổi bật | Ma trận 2 chiều, hàng đợi bằng linked list |
| Thuật toán nổi bật | Tìm vị trí trống gần nhất, Quick Sort |

## 3. Cấu trúc thư mục dự án

```text
QLBaiDoXeThongMinh/
├── doituong/
│   ├── phuong_tien.py
│   ├── loai_xe.py
│   ├── vi_tri_do.py
│   └── loi_ngoai_le.py
├── dulieu/
│   ├── tep_tin.py
│   ├── sap_xep.py
│   ├── lich_su_gui_xe.csv
│   └── lich_su_gui_xe.json
├── giaodien/
│   ├── main.py
│   ├── designer/
│   │   ├── trang_chu.ui
│   │   ├── check_in.ui
│   │   ├── check_out.ui
│   │   ├── quan_ly_bai_xe.ui
│   │   ├── so_do.ui
│   │   ├── thong_tin_xe_ra.ui
│   │   └── uithong_ke_chi_tiet..ui
│   ├── presenters/
│   │   ├── trang_chu_presenter.py
│   │   └── checkin_presenter.py
│   └── views/
│       ├── trang_chu.py
│       ├── check_in.py
│       └── so_do.py
├── xulyhethong/
│   ├── quan_ly_bai_xe.py
│   └── xu_ly_hang_doi.py
└── kiem_thu_thuat_toan.py
```

## 4. Kiến trúc tổng thể

Dự án được tổ chức theo tư duy tách trách nhiệm:

| Lớp | Vai trò |
| --- | --- |
| `doituong` | Định nghĩa các thực thể cốt lõi như phương tiện, xe máy, ô tô, vị trí đỗ và ngoại lệ nghiệp vụ. |
| `xulyhethong` | Chứa logic vận hành bãi xe: khởi tạo sơ đồ bãi, check-in, check-out, tính thống kê, xử lý hàng đợi. |
| `dulieu` | Đọc/ghi lịch sử gửi xe, lưu dữ liệu ra file, sắp xếp dữ liệu lịch sử. |
| `giaodien/views` | Chứa lớp giao diện, nhận thao tác người dùng và phát tín hiệu. |
| `giaodien/presenters` | Điều phối giữa giao diện và hệ thống xử lý, nhận signal từ view và gọi service tương ứng. |
| `giaodien/designer` | Các file giao diện `.ui` được thiết kế bằng Qt Designer. |

Luồng tổng quát:

```text
Người dùng thao tác trên giao diện
        ↓
View phát signal
        ↓
Presenter nhận signal
        ↓
Presenter gọi QuanLyBaiXe
        ↓
QuanLyBaiXe xử lý nghiệp vụ
        ↓
Dữ liệu được cập nhật, lưu file nếu cần
        ↓
Presenter cập nhật lại View
```

## 5. Các lớp đối tượng chính

### 5.1. `PhuongTien`

File: `doituong/phuong_tien.py`

`PhuongTien` là lớp trừu tượng đại diện cho một phương tiện gửi trong bãi xe.

Thuộc tính chính:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `_bien_so` | Biển số xe, được chuẩn hóa bằng cách bỏ khoảng trắng hai đầu và chuyển sang chữ hoa. |
| `_loai_xe` | Loại phương tiện, ví dụ `XeMay` hoặc `OTo`. |
| `_thoi_gian_vao` | Thời điểm xe vào bãi. Nếu không truyền vào thì mặc định là thời điểm hiện tại. |

Logic quan trọng:

- Không cho phép biển số rỗng.
- Thời gian vào phải là đối tượng `datetime`.
- Bắt buộc lớp con phải cài đặt phương thức `tinh_tien_gui`.

### 5.2. `XeMay`

File: `doituong/loai_xe.py`

`XeMay` kế thừa từ `PhuongTien`, đại diện cho xe máy.

Quy tắc tính tiền:

- Giá cố định: `5.000 đ`.
- Tính theo lượt ngày.
- Dùng `math.ceil` để làm tròn lên theo số ngày gửi.
- Nếu gửi dưới 1 ngày vẫn tính tối thiểu 1 lượt.
- Nếu thời gian ra nhỏ hơn thời gian vào thì trả về `0`.

Công thức:

```text
số_lượt = ceil(khoảng_thời_gian_gửi / 24 giờ)
tiền_gửi = max(1, số_lượt) * 5.000
```

### 5.3. `OTo`

File: `doituong/loai_xe.py`

`OTo` kế thừa từ `PhuongTien`, đại diện cho xe ô tô.

Quy tắc tính tiền:

- Giờ đầu: `20.000 đ`.
- Mỗi giờ tiếp theo: `15.000 đ`.
- Thời gian gửi được làm tròn lên theo giờ.
- Nếu thời gian ra nhỏ hơn thời gian vào thì trả về `0`.

Công thức:

```text
nếu tổng_số_giờ <= 1:
    tiền_gửi = 20.000
ngược lại:
    tiền_gửi = 20.000 + (tổng_số_giờ - 1) * 15.000
```

### 5.4. `ViTriDo`

File: `doituong/vi_tri_do.py`

`ViTriDo` đại diện cho một ô đỗ trong bãi xe.

Thuộc tính chính:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `_ma_vi_tri` | Mã vị trí, ví dụ `A01`, `A02`, `B01`. |
| `_loai_slot` | Loại xe được phép đỗ tại vị trí, gồm `XeMay` hoặc `OTo`. |
| `_trang_thai` | Trạng thái ô đỗ, gồm trống hoặc đã có xe. |
| `_xe_dang_do` | Đối tượng xe hiện đang đỗ tại vị trí. |

Phương thức chính:

- `dat_xe(xe)`: đặt xe vào vị trí.
- `trong_xe()`: lấy xe ra khỏi vị trí và đưa vị trí về trạng thái trống.
- `xuat()`: in thông tin vị trí và xe đang đỗ.

Ràng buộc nghiệp vụ:

- Không thể đặt xe vào vị trí đã có xe.
- Không thể đặt sai loại xe vào vị trí không phù hợp.
- Ví dụ: ô dành cho `XeMay` không nhận `OTo`.

### 5.5. Ngoại lệ nghiệp vụ

File: `doituong/loi_ngoai_le.py`

Dự án định nghĩa 2 ngoại lệ riêng:

| Ngoại lệ | Trường hợp sử dụng |
| --- | --- |
| `LotFullError` | Bãi xe hoặc khu vực dành cho loại xe tương ứng đã đầy. |
| `VehicleNotFoundError` | Không tìm thấy xe theo biển số khi check-out hoặc tra cứu. |

Việc dùng ngoại lệ riêng giúp presenter có thể bắt lỗi nghiệp vụ rõ ràng và hiển thị thông báo phù hợp cho người dùng.

## 6. Xử lý hệ thống bãi xe

### 6.1. Lớp `QuanLyBaiXe`

File: `xulyhethong/quan_ly_bai_xe.py`

Đây là lớp trung tâm của toàn bộ hệ thống. Lớp này quản lý sơ đồ bãi xe, xe đang gửi, hàng đợi, lịch sử xe ra, doanh thu và dữ liệu phục vụ giao diện.

Khi khởi tạo:

```python
QuanLyBaiXe(so_hang=8, so_cot=12)
```

Hệ thống mặc định tạo bãi xe gồm:

- `8` hàng.
- `12` cột.
- Tổng cộng `96` vị trí đỗ.
- Nửa trên dành cho xe máy.
- Nửa dưới dành cho ô tô.

### 6.2. Khởi tạo sơ đồ bãi xe

Phương thức:

```python
khoi_tao_bai_xe()
```

Hệ thống tạo một ma trận 2 chiều `so_do_bai_xe`, mỗi phần tử là một đối tượng `ViTriDo`.

Cách chia loại vị trí:

```text
nếu hàng < số_hàng / 2:
    slot dành cho XeMay
ngược lại:
    slot dành cho OTo
```

Cách đặt mã vị trí:

- Khu xe máy được đặt từ `A01`, `A02`, ...
- Khu ô tô cũng được đặt lại theo ký hiệu khu từ `A01`, `A02`, ...
- Mỗi hàng có `12` vị trí.
- Mã vị trí gồm chữ cái khu và số thứ tự cột 2 chữ số.

### 6.3. Tìm vị trí trống gần nhất

Phương thức:

```python
tim_vi_tri_trong_gan_nhat(loai_xe)
```

Logic:

- Duyệt ma trận bãi xe từ hàng đầu đến hàng cuối.
- Trong mỗi hàng, duyệt từ cột đầu đến cột cuối.
- Chỉ chọn slot có:
  - Trạng thái trống.
  - Loại slot trùng với loại xe.
- Vị trí đầu tiên thỏa điều kiện được xem là vị trí gần cổng nhất.

Nếu không còn vị trí phù hợp, hệ thống ném `LotFullError`.

### 6.4. Check-in xe

Phương thức:

```python
check_in_xe(phuong_tien, dua_vao_hang_doi=True)
```

Luồng xử lý:

1. Chuẩn hóa và kiểm tra biển số thông qua đối tượng phương tiện.
2. Kiểm tra biển số đã tồn tại trong bãi hoặc trong hàng đợi chưa.
3. Tìm vị trí trống gần nhất đúng loại xe.
4. Nếu có vị trí:
   - Gọi `dat_xe`.
   - Trả về đối tượng `ViTriDo`.
5. Nếu hết chỗ:
   - Nếu `dua_vao_hang_doi=True`, đưa xe vào hàng đợi.
   - Trả về `None`.
   - Nếu không cho vào hàng đợi, ném `LotFullError`.

Ý nghĩa kết quả trả về:

| Giá trị trả về | Ý nghĩa |
| --- | --- |
| `ViTriDo` | Xe đã được xếp vào một vị trí cụ thể. |
| `None` | Bãi đã đầy và xe đã được đưa vào hàng đợi. |

### 6.5. Check-out xe

Dự án có nhiều phương thức check-out để phục vụ các nhu cầu khác nhau:

| Phương thức | Vai trò |
| --- | --- |
| `check_out_xe(bien_so)` | Giải phóng vị trí và trả về xe. |
| `check_out_xe_kem_vi_tri(bien_so)` | Giải phóng vị trí, trả về xe và mã vị trí. |
| `check_out_va_lap_bien_lai(bien_so, thoi_gian_ra=None)` | Check-out đầy đủ, tính tiền, lưu lịch sử, cập nhật hàng đợi và trả về biên lai. |

Luồng đầy đủ của `check_out_va_lap_bien_lai`:

1. Nhận biển số xe cần ra.
2. Tìm slot đang chứa xe theo biển số.
3. Lấy xe ra khỏi slot.
4. Ghi nhận mã vị trí đã giải phóng.
5. Tính tiền gửi xe dựa trên loại xe và thời gian gửi.
6. Tính số phút gửi.
7. Tạo bản ghi lịch sử.
8. Lưu bản ghi vào CSV và JSON.
9. Kiểm tra hàng đợi:
   - Nếu có xe cùng loại đang chờ, tự động đưa xe đó vào slot vừa trống.
   - Nếu không có xe phù hợp, slot giữ trạng thái trống.
10. Trả về một dictionary chứa thông tin biên lai.

Dữ liệu biên lai gồm:

| Khóa | Ý nghĩa |
| --- | --- |
| `xe_ra` | Đối tượng xe vừa ra khỏi bãi. |
| `ma_vi_tri` | Mã vị trí xe vừa rời đi. |
| `thoi_gian_ra` | Thời điểm xe ra. |
| `so_phut_gui` | Tổng số phút gửi xe. |
| `tien_gui` | Thành tiền. |
| `ban_ghi` | Bản ghi lịch sử dạng dictionary. |
| `xe_vao_tu_hang_doi` | Xe được tự động đưa từ hàng đợi vào vị trí vừa trống, nếu có. |

### 6.6. Tự động đưa xe chờ vào vị trí trống

Phương thức:

```python
_dua_xe_cho_vao_slot_neu_co(slot_trong)
```

Khi một xe check-out, vị trí vừa trống có loại slot xác định. Hệ thống sẽ tìm trong hàng đợi xe đầu tiên có cùng loại với slot đó.

Nếu tìm thấy:

- Xe được lấy khỏi hàng đợi.
- Xe được đặt vào slot vừa trống.
- Hàm trả về xe vừa được đưa vào.

Nếu không tìm thấy:

- Không làm gì thêm.
- Hàm trả về `None`.

Điểm tốt của logic này là bãi xe tự động phục vụ xe đang chờ, không cần người dùng thao tác check-in lại.

### 6.7. Kiểm tra trùng biển số

Phương thức:

```python
_bien_so_da_ton_tai(bien_so)
```

Hệ thống kiểm tra biển số ở 2 nơi:

- Xe đang nằm trong bãi.
- Xe đang nằm trong hàng đợi.

Nếu biển số đã tồn tại, thao tác check-in bị từ chối để tránh một xe xuất hiện nhiều lần trong hệ thống.

## 7. Hàng đợi xe chờ

File: `xulyhethong/xu_ly_hang_doi.py`

Hệ thống tự cài đặt hàng đợi bằng linked list.

### 7.1. Lớp `Node`

Mỗi `Node` đại diện cho một xe đang đứng trong hàng đợi.

Thuộc tính:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `data` | Đối tượng xe. |
| `next` | Liên kết đến node kế tiếp. |

### 7.2. Lớp `HangDoiXeCho`

Đây là cấu trúc hàng đợi tự cài đặt theo cơ chế FIFO.

Thuộc tính:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `head` | Xe đầu hàng đợi. |
| `tail` | Xe cuối hàng đợi. |
| `_size` | Số lượng xe đang chờ. |

Phương thức chính:

| Phương thức | Chức năng |
| --- | --- |
| `enqueue(phuong_tien)` | Thêm xe vào cuối hàng đợi. |
| `dequeue()` | Lấy xe đầu hàng đợi ra. |
| `dequeue_theo_loai(loai_xe)` | Lấy xe đầu tiên đúng loại xe. |
| `is_empty()` | Kiểm tra hàng đợi rỗng. |
| `size()` | Trả về số lượng xe đang chờ. |
| `dem_theo_loai(loai_xe)` | Đếm số xe đang chờ theo loại. |
| `to_list()` | Chuyển hàng đợi thành danh sách Python. |

### 7.3. Điểm đặc biệt của `dequeue_theo_loai`

Thay vì luôn lấy xe đầu tiên tuyệt đối, hệ thống lấy xe đầu tiên có loại phù hợp với slot vừa trống.

Ví dụ:

```text
Hàng đợi: Xe máy A -> Ô tô B -> Xe máy C
Slot vừa trống: Ô tô
Kết quả: Ô tô B được lấy ra, Xe máy A và Xe máy C vẫn giữ thứ tự tương đối.
```

Điều này giúp tránh đưa sai loại xe vào khu vực không phù hợp.

## 8. Lưu trữ dữ liệu

File: `dulieu/tep_tin.py`

Dữ liệu lịch sử xe ra được lưu song song vào 2 định dạng:

- `dulieu/lich_su_gui_xe.csv`
- `dulieu/lich_su_gui_xe.json`

### 8.1. Cấu trúc bản ghi lịch sử

Mỗi bản ghi gồm các cột:

| Cột | Ý nghĩa |
| --- | --- |
| `bien_so` | Biển số xe. |
| `loai_xe` | Loại xe hiển thị, ví dụ `Xe máy` hoặc `Ô tô`. |
| `vi_tri` | Mã vị trí đỗ. |
| `gio_vao` | Thời điểm xe vào. |
| `gio_ra` | Thời điểm xe ra. |
| `so_phut_gui` | Tổng số phút gửi. |
| `thanh_tien` | Số tiền phải thanh toán. |

### 8.2. Đọc lịch sử CSV

Phương thức:

```python
doc_lich_su_csv()
```

Chức năng:

- Nếu file CSV chưa tồn tại, trả về danh sách rỗng.
- Nếu file tồn tại, đọc bằng `csv.DictReader`.
- Sử dụng encoding `utf-8-sig` để xử lý tốt file có BOM.

### 8.3. Ghi thêm lịch sử CSV

Phương thức:

```python
ghi_them_lich_su_csv(ban_ghi)
```

Chức năng:

- Tạo thư mục dữ liệu nếu chưa có.
- Nếu file rỗng hoặc chưa tồn tại thì ghi header.
- Ghi thêm một dòng lịch sử mới.

### 8.4. Đọc và ghi JSON

Các phương thức:

```python
doc_lich_su_json()
ghi_lich_su_json(danh_sach_ban_ghi)
```

Chức năng:

- JSON lưu toàn bộ danh sách lịch sử.
- Nếu JSON lỗi định dạng, hệ thống trả về danh sách rỗng để tránh crash.
- Khi lưu, dùng `ensure_ascii=False` để hỗ trợ tiếng Việt.

### 8.5. Lưu bản ghi lịch sử đầy đủ

Phương thức:

```python
luu_ban_ghi_lich_su(ban_ghi)
```

Chức năng:

- Ghi thêm bản ghi vào CSV.
- Đọc danh sách JSON hiện có.
- Thêm bản ghi mới vào danh sách.
- Ghi lại file JSON.

## 9. Thuật toán sắp xếp

File: `dulieu/sap_xep.py`

Dự án tự cài đặt thuật toán Quick Sort để sắp xếp dữ liệu lịch sử.

### 9.1. Hàm `quick_sort`

```python
quick_sort(danh_sach, key, reverse=True)
```

Đặc điểm:

- Nhận danh sách dict hoặc object.
- Nhận `key` dạng tên thuộc tính/tên khóa hoặc callable.
- Mặc định sắp xếp giảm dần.
- Chọn pivot ở giữa danh sách.
- Chia dữ liệu thành 3 nhóm:
  - Nhỏ hơn pivot.
  - Bằng pivot.
  - Lớn hơn pivot.

### 9.2. Sắp xếp theo thời gian gửi

```python
sap_xep_theo_thoi_gian_gui(danh_sach_lich_su)
```

Sắp xếp lịch sử theo `so_phut_gui` giảm dần. Dùng để tìm các lượt gửi xe lâu nhất.

### 9.3. Sắp xếp theo doanh thu

```python
sap_xep_theo_doanh_thu(danh_sach_lich_su)
```

Sắp xếp lịch sử theo `thanh_tien` giảm dần. Dùng để tìm các lượt gửi xe có doanh thu cao nhất.

## 10. Các chức năng thống kê

Trong `QuanLyBaiXe`, hệ thống cung cấp nhiều hàm lấy dữ liệu thống kê:

| Phương thức | Ý nghĩa |
| --- | --- |
| `lay_tong_so_xe_dang_gui()` | Đếm tổng số xe đang ở trong bãi. |
| `lay_so_xe_theo_loai(loai_xe)` | Đếm số xe đang gửi theo loại xe. |
| `lay_so_xe_cho_theo_loai(loai_xe)` | Đếm số xe đang chờ theo loại xe. |
| `lay_tong_so_o()` | Tổng số ô đỗ trong bãi. |
| `lay_so_o_trong()` | Số ô còn trống. |
| `lay_ty_le_lap_day()` | Tính phần trăm lấp đầy của bãi. |
| `lay_doanh_thu_theo_ngay(ngay=None)` | Tính doanh thu theo ngày. |
| `lay_lich_su_gui_lau_nhat()` | Lấy lịch sử được sắp theo thời gian gửi giảm dần. |
| `lay_lich_su_doanh_thu_cao_nhat()` | Lấy lịch sử được sắp theo thành tiền giảm dần. |

Công thức tỷ lệ lấp đầy:

```text
tỷ_lệ_lấp_đầy = số_xe_đang_gửi / tổng_số_ô * 100
```

Doanh thu theo ngày được tính bằng cách duyệt lịch sử xe ra, parse `gio_ra`, so sánh ngày và cộng `thanh_tien`.

## 11. Giao diện người dùng

Giao diện được thiết kế bằng Qt Designer và nạp vào chương trình bằng `uic.loadUi`.

### 11.1. Entry point

File: `giaodien/main.py`

Vai trò:

- Tạo `QApplication`.
- Thiết lập stylesheet chung cho `QMessageBox`.
- Tạo view `TrangChu`.
- Tạo presenter `TrangChuPresenter`.
- Gọi `presenter.load()`.
- Hiển thị màn hình chính.
- Chạy vòng lặp ứng dụng bằng `app.exec_()`.

### 11.2. Màn hình trang chủ

File giao diện: `giaodien/designer/trang_chu.ui`  
File view: `giaodien/views/trang_chu.py`

Trang chủ là màn hình chính của hệ thống.

Thành phần chính:

| Thành phần | Chức năng |
| --- | --- |
| `btn_checkin` | Mở màn hình check-in xe vào. |
| `btn_checkout` | Mở màn hình check-out xe ra. |
| `btn_quan_ly_bai_xe` | Mở danh sách xe đang gửi. |
| `btn_thong_ke_chi_tiet` | Mở phần lịch sử/thống kê chi tiết. |
| `btn_so_do_b1` | Mở sơ đồ tầng B1. |
| `btn_so_do_b2` | Mở sơ đồ tầng B2. |
| `lbl_xe_may_2` | Hiển thị số xe máy đang gửi. |
| `lbl_o_to_2` | Hiển thị số ô tô đang gửi. |
| `lbl_xe_may_cho` | Hiển thị số xe máy đang chờ. |
| `lbl_o_to_cho` | Hiển thị số ô tô đang chờ. |
| `lbl_doanh_thu` | Hiển thị doanh thu hôm nay. |
| `donutLabel` | Hiển thị tỷ lệ lấp đầy và số xe trên tổng số ô. |

View không trực tiếp xử lý nghiệp vụ. View chỉ:

- Kết nối nút với signal.
- Cung cấp phương thức hiển thị dữ liệu.
- Phát tín hiệu cho presenter khi người dùng thao tác.

### 11.3. Màn hình check-in

File giao diện: `giaodien/designer/check_in.ui`  
File view: `giaodien/views/check_in.py`  
File presenter: `giaodien/presenters/checkin_presenter.py`

Chức năng:

- Nhập biển số xe.
- Chọn loại xe: xe máy hoặc ô tô.
- Xác nhận check-in.
- Hiển thị lỗi nếu biển số rỗng hoặc xe không hợp lệ.
- Hiển thị thông báo nếu xe được xếp vào bãi hoặc phải vào hàng đợi.

Luồng xử lý:

```text
Người dùng nhập biển số và chọn loại xe
        ↓
Bấm CHECK-IN
        ↓
CheckInDialog phát signal yeu_cau_xac_nhan
        ↓
CheckInPresenter.xu_ly_check_in()
        ↓
Tạo XeMay hoặc OTo
        ↓
Gọi QuanLyBaiXe.check_in_xe()
        ↓
Cập nhật dashboard
        ↓
Đóng dialog nếu thành công
```

Kiểm tra dữ liệu:

- Nếu biển số rỗng, presenter gọi `bao_loi`.
- Nếu biển số trùng hoặc bãi xử lý lỗi, presenter bắt exception và hiển thị thông báo.

### 11.4. Màn hình check-out

File giao diện: `giaodien/designer/check_out.ui`  
Logic xử lý: `giaodien/presenters/trang_chu_presenter.py`

Chức năng:

- Nhập biển số xe cần ra.
- Bấm `CHECK-OUT`.
- Hệ thống tìm xe trong bãi.
- Tính tiền gửi xe.
- Lưu lịch sử.
- Cập nhật dashboard.
- Mở màn hình thông tin xe ra.

Luồng xử lý:

```text
Người dùng nhập biển số
        ↓
Bấm CHECK-OUT
        ↓
TrangChuPresenter._xu_ly_check_out()
        ↓
QuanLyBaiXe.check_out_va_lap_bien_lai()
        ↓
Cập nhật dashboard
        ↓
Mở dialog thông tin xe ra
```

Nếu không tìm thấy biển số, hệ thống hiển thị cảnh báo `VehicleNotFoundError`.

### 11.5. Màn hình thông tin xe ra

File giao diện: `giaodien/designer/thong_tin_xe_ra.ui`

Màn hình này đóng vai trò như biên lai sau khi check-out.

Thông tin hiển thị:

| Nhãn | Ý nghĩa |
| --- | --- |
| `lbl_bien_so` | Biển số xe. |
| `lbl_loai_xe` | Loại xe. |
| `lbl_vi_tri_do` | Vị trí đỗ trước khi ra. |
| `lbl_gio_vao` | Giờ vào bãi. |
| `lbl_gio_ra` | Giờ ra bãi. |
| `lbl_thoi_gian_gui` | Tổng thời gian gửi dạng giờ/phút. |
| `lbl_thanh_tien` | Tổng tiền cần thanh toán. |

Nếu sau khi xe ra có xe trong hàng đợi được tự động đưa vào vị trí vừa trống, hệ thống hiển thị thêm thông báo cho người dùng.

### 11.6. Màn hình quản lý bãi xe

File giao diện: `giaodien/designer/quan_ly_bai_xe.ui`

Màn hình gồm 2 tab:

| Tab | Nội dung |
| --- | --- |
| `DANH SÁCH XE ĐANG GỬI` | Bảng xe hiện đang ở trong bãi. |
| `LỊCH SỬ XE ĐÃ RA` | Bảng lịch sử các lượt xe đã check-out. |

Bảng xe đang gửi gồm:

- Biển số.
- Loại xe.
- Vị trí.
- Giờ vào.
- Hành động.

Bảng lịch sử xe đã ra gồm:

- Biển số.
- Loại xe.
- Vị trí.
- Giờ vào.
- Giờ ra.
- Thành tiền.

Dữ liệu được đổ vào bảng bằng phương thức `_do_du_lieu_bang` trong `TrangChuPresenter`.

### 11.7. Màn hình sơ đồ bãi xe

File giao diện: `giaodien/designer/so_do.ui`

Màn hình sơ đồ gồm 2 tab:

| Tab | Ý nghĩa |
| --- | --- |
| `Tầng B1` | Hiển thị khu vực xe máy. |
| `Tầng B2` | Hiển thị khu vực ô tô. |

Presenter vẽ sơ đồ bằng cách:

- Lấy dữ liệu slot từ `QuanLyBaiXe`.
- Tạo `QPushButton` cho từng vị trí đỗ.
- Gắn màu theo trạng thái:
  - Xanh: còn trống.
  - Đỏ: đã có xe.
- Khi bấm vào một ô, hiển thị thông tin vị trí và biển số nếu có xe.

Dữ liệu sơ đồ lấy từ:

```python
lay_du_lieu_theo_loai_slot("XeMay")
lay_du_lieu_theo_loai_slot("OTo")
```

### 11.8. Màn hình thống kê chi tiết

File giao diện: `giaodien/designer/uithong_ke_chi_tiet..ui`

File này định nghĩa giao diện thống kê chi tiết gồm:

- Chọn ngày.
- Tổng số xe.
- Số xe máy.
- Số xe ô tô.
- Doanh thu.

Trong phiên bản hiện tại, nút `LỊCH SỬ` trên trang chủ đang mở màn hình quản lý bãi xe ở tab lịch sử. File thống kê chi tiết đã có giao diện nhưng chưa thấy được kết nối đầy đủ vào presenter hiện tại.

## 12. Presenter và vai trò điều phối

### 12.1. `TrangChuPresenter`

File: `giaodien/presenters/trang_chu_presenter.py`

Đây là presenter chính của ứng dụng.

Nhiệm vụ:

- Tạo đối tượng `QuanLyBaiXe`.
- Kết nối signal từ trang chủ với các hàm xử lý.
- Mở dialog check-in.
- Mở dialog check-out.
- Mở màn hình quản lý bãi xe.
- Mở màn hình sơ đồ.
- Cập nhật dashboard.
- Đổ dữ liệu vào bảng xe đang gửi và lịch sử.
- Tạo các nút vị trí đỗ trên sơ đồ.

Các signal được kết nối:

| Signal từ view | Hàm xử lý |
| --- | --- |
| `yeu_cau_checkin` | `mo_man_hinh_check_in` |
| `yeu_cau_checkout` | `mo_man_hinh_check_out` |
| `yeu_cau_quan_ly_bai_xe` | `mo_man_hinh_quan_ly_bai_xe` |
| `yeu_cau_thong_ke_chi_tiet` | `mo_man_hinh_thong_ke_chi_tiet` |
| `yeu_cau_so_do` | `mo_man_hinh_so_do` |

### 12.2. `CheckInPresenter`

File: `giaodien/presenters/checkin_presenter.py`

Nhiệm vụ:

- Nhận dữ liệu từ `CheckInDialog`.
- Kiểm tra biển số rỗng.
- Tạo đối tượng `XeMay` hoặc `OTo`.
- Gọi `QuanLyBaiXe.check_in_xe`.
- Hiển thị thông báo kết quả.
- Gọi callback cập nhật dashboard nếu check-in thành công.
- Đóng dialog.

## 13. Các luồng nghiệp vụ chính

### 13.1. Luồng check-in thành công

```text
1. Người dùng mở màn hình check-in.
2. Nhập biển số.
3. Chọn loại xe.
4. Hệ thống tạo đối tượng phương tiện.
5. Hệ thống kiểm tra biển số trùng.
6. Hệ thống tìm vị trí trống gần nhất đúng loại xe.
7. Xe được đặt vào vị trí.
8. Dashboard cập nhật số xe đang gửi, số xe chờ, tỷ lệ lấp đầy.
9. Dialog đóng.
```

### 13.2. Luồng check-in khi bãi đầy

```text
1. Người dùng check-in xe.
2. Hệ thống tìm vị trí trống đúng loại.
3. Không còn vị trí phù hợp.
4. Xe được đưa vào hàng đợi.
5. Hệ thống thông báo xe đã vào hàng đợi.
6. Dashboard cập nhật số xe đang chờ.
```

### 13.3. Luồng check-out thành công

```text
1. Người dùng mở màn hình check-out.
2. Nhập biển số.
3. Hệ thống tìm xe trong bãi.
4. Xe được lấy khỏi vị trí.
5. Hệ thống tính thời gian gửi.
6. Hệ thống tính tiền gửi theo loại xe.
7. Lịch sử được lưu vào CSV và JSON.
8. Nếu có xe chờ cùng loại, xe đó được đưa vào slot vừa trống.
9. Dashboard và bảng quản lý được cập nhật.
10. Màn hình thông tin xe ra hiển thị biên lai.
```

### 13.4. Luồng check-out khi không tìm thấy xe

```text
1. Người dùng nhập biển số.
2. Hệ thống duyệt toàn bộ bãi xe.
3. Không tìm thấy xe có biển số tương ứng.
4. Hệ thống ném VehicleNotFoundError.
5. Presenter hiển thị cảnh báo cho người dùng.
```

## 14. Dữ liệu phục vụ giao diện

`QuanLyBaiXe` có nhiều phương thức chuyển dữ liệu nội bộ thành dictionary/list để giao diện dễ đọc.

### 14.1. Dữ liệu sơ đồ

```python
lay_du_lieu_so_do_cho_gui()
```

Trả về ma trận dictionary:

```python
{
    "ma_vi_tri": "A01",
    "loai_slot": "XeMay",
    "trang_thai": "Trống",
    "bien_so": ""
}
```

### 14.2. Danh sách xe đang gửi

```python
lay_danh_sach_xe_dang_gui()
```

Trả về danh sách:

```python
{
    "bien_so": "38A-12345",
    "loai_xe": "Ô tô",
    "vi_tri": "A01",
    "gio_vao": "22/06/2026 09:30"
}
```

### 14.3. Danh sách xe chờ

```python
lay_danh_sach_xe_cho()
```

Trả về danh sách xe trong hàng đợi:

```python
{
    "bien_so": "38A-12345",
    "loai_xe": "Ô tô",
    "gio_vao": "22/06/2026 09:30"
}
```

### 14.4. Lịch sử xe ra

```python
lay_lich_su_xe_ra()
```

Trả về dữ liệu lịch sử đã được format:

- Giờ vào/giờ ra hiển thị dạng `dd/mm/YYYY HH:MM`.
- Thành tiền hiển thị có dấu phân tách hàng nghìn và ký hiệu `đ`.

## 15. Kiểm thử thuật toán

File: `kiem_thu_thuat_toan.py`

File này dùng để kiểm thử nhanh các logic quan trọng mà không cần chạy giao diện.

Các phần được kiểm thử:

- Khởi tạo bãi xe.
- Check-in xe máy và ô tô.
- Tìm vị trí gần cổng.
- Đưa xe vào hàng đợi khi khu vực xe tương ứng đầy.
- Check-out, tính tiền và lưu lịch sử.
- Tự động đưa xe từ hàng đợi vào vị trí vừa trống.
- Sắp xếp bằng Quick Sort theo thời gian gửi.
- Sắp xếp bằng Quick Sort theo doanh thu.
- Thống kê tổng số xe đang gửi.
- Tính tỷ lệ lấp đầy.

Có thể chạy bằng:

```bash
python kiem_thu_thuat_toan.py
```

## 16. Điểm mạnh của dự án

- Có tách lớp giữa giao diện, presenter và xử lý nghiệp vụ.
- Logic check-in/check-out tương đối đầy đủ.
- Có kiểm tra trùng biển số.
- Có ngoại lệ nghiệp vụ riêng.
- Có hàng đợi tự cài đặt bằng linked list.
- Có tự động đưa xe chờ vào vị trí vừa trống.
- Có lưu lịch sử vào cả CSV và JSON.
- Có dashboard hiển thị số xe, xe chờ, doanh thu và tỷ lệ lấp đầy.
- Có sơ đồ bãi xe trực quan theo màu.
- Có file kiểm thử thuật toán riêng.

## 17. Một số điểm cần lưu ý

### 17.1. Mã hóa tiếng Việt trong một số file Python

Khi đọc mã nguồn, một số chuỗi tiếng Việt trong file `.py` đang hiển thị sai encoding, ví dụ các chữ có dấu bị biến thành ký tự lạ. Tuy nhiên, các file `.ui` lại hiển thị tiếng Việt đúng.

Nên thống nhất toàn bộ mã nguồn về UTF-8 để tránh lỗi hiển thị thông báo trên giao diện.

### 17.2. Dữ liệu xe đang gửi chưa được lưu bền vững

Hiện tại hệ thống chỉ lưu lịch sử xe đã ra. Danh sách xe đang gửi trong bãi và hàng đợi chỉ tồn tại trong RAM khi chương trình đang chạy.

Nếu tắt ứng dụng, trạng thái xe đang gửi sẽ mất.

Hướng cải thiện:

- Lưu trạng thái bãi xe hiện tại vào JSON.
- Khi mở ứng dụng, khôi phục trạng thái từ file.
- Lưu cả hàng đợi để không mất xe chờ.

### 17.3. Màn hình thống kê chi tiết chưa được tích hợp đầy đủ

File `uithong_ke_chi_tiet..ui` đã tồn tại, nhưng presenter hiện tại chưa mở trực tiếp dialog này. Nút lịch sử đang mở màn hình quản lý bãi xe ở tab lịch sử.

Có thể phát triển thêm presenter riêng cho thống kê chi tiết.

### 17.4. Nút hành động trong bảng xe đang gửi chưa check-out trực tiếp

Bảng xe đang gửi có cột `HÀNH ĐỘNG` với giá trị `CHECK-OUT`, nhưng hiện tại đang được đổ như text trong `QTableWidgetItem`, chưa phải button có thể bấm.

Hướng cải thiện:

- Tạo `QPushButton` trong từng dòng.
- Khi bấm, gọi check-out theo biển số của dòng đó.
- Cập nhật bảng và dashboard sau khi hoàn tất.

### 17.5. File giao diện thống kê có tên chưa gọn

File:

```text
giaodien/designer/uithong_ke_chi_tiet..ui
```

Tên file có 2 dấu chấm trước `.ui`. Nên đổi thành:

```text
thong_ke_chi_tiet.ui
```

Sau đó cập nhật lại đường dẫn trong code nếu tích hợp màn hình này.

## 18. Gợi ý hướng phát triển tiếp theo

Một số hướng nâng cấp hợp lý:

- Lưu và khôi phục trạng thái xe đang gửi sau khi tắt ứng dụng.
- Thêm chức năng tìm kiếm xe theo biển số.
- Thêm lọc lịch sử theo ngày, loại xe, khoảng thời gian.
- Thêm thống kê doanh thu theo ngày, tuần, tháng.
- Thêm biểu đồ doanh thu.
- Thêm cấu hình giá gửi xe từ giao diện.
- Thêm quản lý nhiều tầng/khu vực linh hoạt hơn.
- Thêm xác nhận trước khi check-out.
- Thêm in vé hoặc xuất biên lai PDF.
- Thêm đăng nhập và phân quyền nhân viên/quản trị.
- Thêm kiểm thử tự động bằng `pytest`.
- Chuẩn hóa toàn bộ encoding tiếng Việt về UTF-8.

## 19. Kết luận

Dự án `QLBaiDoXeThongMinh` là một hệ thống quản lý bãi xe thông minh ở mức mô phỏng khá đầy đủ, có đủ các nghiệp vụ cốt lõi của một bãi xe: xe vào, xe ra, xếp vị trí, hàng đợi, tính phí, lưu lịch sử và thống kê. Cách tổ chức mã nguồn theo nhiều lớp giúp dự án dễ hiểu, dễ mở rộng và phù hợp để phát triển tiếp thành một ứng dụng quản lý bãi xe hoàn chỉnh hơn.

Phần lõi quan trọng nhất của dự án nằm ở `QuanLyBaiXe`, nơi kết hợp mô hình vị trí đỗ, phương tiện, hàng đợi, lịch sử và thống kê. Phần giao diện PyQt5 giúp người dùng thao tác trực quan, còn các file dữ liệu CSV/JSON giúp lưu lại lịch sử gửi xe để phục vụ thống kê và kiểm tra sau này.
