# HƯỚNG DẪN CHẠY DỰ ÁN


Tài liệu này dành cho người vừa nhận được source code dự án `QLBaiDoXeThongMinh` và cần chạy được chương trình trên máy cá nhân.


## 1. Yêu cầu trước khi chạy


Cần cài sẵn:


- Python 3.10 trở lên.
- `pip`.
- Terminal hoặc Command Prompt/PowerShell.
- Visual Studio Code hoặc IDE Python bất kỳ.


Kiểm tra Python:


```bash
python --version
```


Kiểm tra pip:


```bash
pip --version
```


Nếu máy dùng nhiều phiên bản Python, có thể cần dùng:


```bash
py --version
py -m pip --version
```


## 2. Mở đúng thư mục dự án


Di chuyển vào thư mục gốc của project:


```bash
cd "D:\Source Code\project_HeThongQuanLyBaiXeThongMinh\QLBaiDoXeThongMinh"
```


Nếu bạn giải nén dự án ở vị trí khác, hãy thay đường dẫn trên bằng đường dẫn thực tế trên máy.


Thư mục đúng là thư mục chứa các folder:


```text
doituong/
dulieu/
giaodien/
xulyhethong/
kiem_thu_thuat_toan.py
```


## 3. Tạo môi trường ảo


Nên tạo môi trường ảo để thư viện của dự án không ảnh hưởng tới Python hệ thống.


Trên Windows:


```bash
python -m venv .venv
```


Hoặc:


```bash
py -m venv .venv
```


Kích hoạt môi trường ảo bằng PowerShell:


```bash
.\.venv\Scripts\Activate.ps1
```


Nếu dùng Command Prompt:


```bash
.\.venv\Scripts\activate.bat
```


Khi kích hoạt thành công, terminal thường sẽ hiện tiền tố:


```text
(.venv)
```


## 4. Cài thư viện cần thiết


Dự án dùng PyQt5 để chạy giao diện.


Cài PyQt5:


```bash
pip install PyQt5
```


Nếu dùng lệnh `py`:


```bash
py -m pip install PyQt5
```


Kiểm tra PyQt5 đã cài được chưa:


```bash
python -c "import PyQt5; print('PyQt5 OK')"
```


Nếu terminal in ra:


```text
PyQt5 OK
```


thì thư viện đã được cài thành công.


## 5. Chạy chương trình giao diện


Từ thư mục gốc dự án, chạy:


```bash
python giaodien\main.py
```


Hoặc:


```bash
py giaodien\main.py
```


Sau khi chạy, màn hình chính của hệ thống quản lý bãi xe sẽ mở lên.


## 6. Chạy file kiểm thử thuật toán


Dự án có file kiểm thử nhanh các logic chính:


```bash
python kiem_thu_thuat_toan.py
```


Hoặc:


```bash
py kiem_thu_thuat_toan.py
```


File này kiểm thử:


- Khởi tạo bãi xe.
- Check-in xe.
- Check-out xe.
- Tính tiền gửi xe.
- Đưa xe vào hàng đợi khi đầy.
- Tự động đưa xe chờ vào slot trống.
- Sắp xếp lịch sử bằng Quick Sort.
- Tính thống kê cơ bản.


## 7. Các lệnh chạy nhanh


Nếu chạy lần đầu trên Windows PowerShell:


```bash
cd "D:\Source Code\project_HeThongQuanLyBaiXeThongMinh\QLBaiDoXeThongMinh"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install PyQt5
python giaodien\main.py
```


Nếu đã cài thư viện và chỉ muốn mở lại chương trình:


```bash
cd "D:\Source Code\project_HeThongQuanLyBaiXeThongMinh\QLBaiDoXeThongMinh"
.\.venv\Scripts\Activate.ps1
python giaodien\main.py
```


## 8. Dữ liệu được lưu ở đâu?


Lịch sử xe ra được lưu trong thư mục:


```text
dulieu/
```


Các file dữ liệu chính:


```text
dulieu/lich_su_gui_xe.csv
dulieu/lich_su_gui_xe.json
```


Khi check-out xe thành công, hệ thống sẽ ghi thêm lịch sử vào các file này.


Lưu ý: danh sách xe đang gửi hiện chỉ nằm trong bộ nhớ khi chương trình đang chạy. Nếu tắt app, trạng thái xe đang gửi trong bãi sẽ không được khôi phục, nhưng lịch sử xe đã ra vẫn được lưu.


## 9. Lỗi thường gặp và cách xử lý


### 9.1. Lỗi `ModuleNotFoundError: No module named 'PyQt5'`


Nguyên nhân: chưa cài PyQt5 hoặc đang chạy sai môi trường Python.


Cách xử lý:


```bash
pip install PyQt5
```


Nếu dùng môi trường ảo, hãy kích hoạt `.venv` trước rồi cài lại.


### 9.2. Không chạy được lệnh kích hoạt môi trường ảo trên PowerShell


Nếu gặp lỗi liên quan đến Execution Policy, chạy:


```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


Sau đó kích hoạt lại:


```bash
.\.venv\Scripts\Activate.ps1
```


Lệnh này chỉ thay đổi chính sách thực thi trong phiên terminal hiện tại.


### 9.3. Lỗi không tìm thấy file `.ui`


Nguyên nhân thường là chạy sai thư mục hoặc di chuyển cấu trúc dự án.


Cách xử lý:


- Đảm bảo đang đứng ở thư mục gốc `QLBaiDoXeThongMinh`.
- Không đổi tên thư mục `giaodien/designer`.
- Chạy bằng:


```bash
python giaodien\main.py
```


### 9.4. Chữ tiếng Việt hiển thị lỗi trong terminal


Một số terminal Windows có thể hiển thị tiếng Việt không đúng encoding. Có thể thử:


```bash
chcp 65001
```


Sau đó chạy lại chương trình hoặc file kiểm thử.


Giao diện PyQt5 thường vẫn hiển thị đúng nếu file `.ui` được lưu UTF-8.


## 10. Tóm tắt lệnh cần nhớ


Cài và chạy lần đầu:


```bash
cd "D:\Source Code\project_HeThongQuanLyBaiXeThongMinh\QLBaiDoXeThongMinh"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install PyQt5
python giaodien\main.py
```


Chạy lại sau khi đã cài:


```bash
cd "D:\Source Code\project_HeThongQuanLyBaiXeThongMinh\QLBaiDoXeThongMinh"
.\.venv\Scripts\Activate.ps1
python giaodien\main.py
```


Chạy kiểm thử logic:


```bash
python kiem_thu_thuat_toan.py
```




