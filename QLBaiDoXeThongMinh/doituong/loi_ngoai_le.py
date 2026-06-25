class LotFullError(Exception):
    def __init__(self, message="Lỗi: Bãi đỗ xe đã đầy!"):
        self.message = message
        super().__init__(self.message)
class VehicleNotFoundError(Exception):
    def __init__(self, message="Lỗi: Không tìm thấy phương tiện trong bãi!"):
        self.message = message
        super().__init__(self.message)
