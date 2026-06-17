"""
Tầng Presenter
Cầu nối: Lấy dữ liệu từ Service -> đẩy vào View: Nhận signal từ view -> xử lý
nguyên tắc là View và Service không biết gì nhau

"""
from views.trang_chu import ITrangChuView
from views.check_in import CheckInDialog
from presenters.checkin_presenter import CheckInPresenter


class TrangChuPresenter: 
    def __init__(self, view:ITrangChuView):
        self._view = view
        self._noi_su_kien()

    def _noi_su_kien(self):
        self._view.yeu_cau_checkin.connect(self.mo_man_hinh_check_in)

    def load(self):
        # fake du lieu tu Service 
        MOCK = {
            "xe_may" : 4100,
            "oto" : 32,
            "doanh_thu" : 300000,
            "xe_may_cho" : 100,
            "xe_oto_cho" : 10,
            "tong_ve" : 210,
        }

        self._view.hien_so_xe(MOCK["xe_may"],MOCK["oto"])
        self._view.hien_doanh_thu(MOCK["doanh_thu"])
        self._view.hien_xe_cho(MOCK["xe_may_cho"],MOCK["xe_oto_cho"])


        

    def mo_man_hinh_check_in(self):
        dialog = CheckInDialog()
        presenter = CheckInPresenter(dialog)
        dialog.exec_()
