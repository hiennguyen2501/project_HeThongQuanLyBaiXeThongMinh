from views.check_in import ICheckinView

class CheckInPresenter:
    def __init__(self, view:ICheckinView):
        self._view = view
        self._view.yeu_cau_xac_nhan.connect(self.xu_ly_check_in)

    def xu_ly_check_in(self):
        bien_so = self._view.lay_bien_so().strip()
        if not bien_so:
            self._view.bao_loi("Vui Long Nhap Bien So")
            return
        
        loai_xe = self._view.lay_loai_xe()
        #Gọi service
        from logic_handler import check_in
        check_in(bien_so)
        print("Bien so", bien_so)
        print("Loai Xe", loai_xe)
        #
        self._view.dong_thanh_cong()