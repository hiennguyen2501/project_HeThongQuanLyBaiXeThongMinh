class LotFullError(Exception):
    """
    Ngoại lệ thông báo khi bãi xe không còn vị trí trống cho loại xe tương ứng.
    """
    def __init__(self, message="Lỗi: Bãi đỗ xe đã đầy!"):
        self.message = message
        super().__init__(self.message)
class VehicleNotFoundError(Exception):
    """
    Ngoại lệ khi nhập biển số xe không có trong bãi.
    """
    def __init__(self, message="Lỗi: Không tìm thấy phương tiện trong bãi!"):
        self.message = message
        super().__init__(self.message)
        
