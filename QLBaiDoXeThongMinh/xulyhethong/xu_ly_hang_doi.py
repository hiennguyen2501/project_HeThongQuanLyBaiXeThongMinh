class Node:
    def __init__(self, phuong_tien):
        self.data = phuong_tien
        self.next = None


class HangDoiXeCho:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0


    def enqueue(self, phuong_tien):
        new_node = Node(phuong_tien)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1


    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return temp.data


    def dequeue_theo_loai(self, loai_xe):
        previous = None
        current = self.head


        while current is not None:
            if current.data.loai_xe == loai_xe:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current == self.tail:
                    self.tail = previous
                self._size -= 1
                return current.data
            previous = current
            current = current.next


        return None


    def is_empty(self):
        return self.head is None


    def size(self):
        return self._size


    def dem_theo_loai(self, loai_xe):
        dem = 0
        current = self.head
        while current is not None:
            if current.data.loai_xe == loai_xe:
                dem += 1
            current = current.next
        return dem


    def to_list(self):
        danh_sach = []
        current = self.head
        while current is not None:
            danh_sach.append(current.data)
            current = current.next
        return danh_sach
