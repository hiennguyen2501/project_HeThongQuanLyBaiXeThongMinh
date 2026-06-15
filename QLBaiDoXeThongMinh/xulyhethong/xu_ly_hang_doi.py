class Node:
    """Mỗi Node đại diện cho một xe đang đứng trong hàng đợi"""
    def __init__(self, phuong_tien):
        self.data = phuong_tien  # Đối tượng XeMay hoặc OTo do Thành viên 1 định nghĩa
        self.next = None         # Liên kết đến xe đứng sau

class HangDoiXeCho:
    """Cấu trúc dữ liệu Hàng đợi tự cài đặt (Linked List dựa trên cơ chế FIFO)"""
    def __init__(self):
        self.head = None  # Xe đứng đầu hàng
        self.tail = None  # Xe đứng cuối háng
        self._size = 0    # Số lượng xe đang chờ ngoài cổng

    def enqueue(self, phuong_tien):
        """Thêm xe mới vào cuối hàng đợi khi bãi đầy"""
        new_node = Node(phuong_tien)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        """Lấy xe ở đầu hàng đợi ra khi bãi trống chỗ"""
        if self.is_empty():
            return None
        temp = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return temp.data

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size