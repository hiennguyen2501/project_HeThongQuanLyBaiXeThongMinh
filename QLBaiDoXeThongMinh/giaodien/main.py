from PyQt5.QtWidgets import QApplication
from datetime import datetime, timedelta
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from doituong.loai_xe import OTo, XeMay
from dulieu.du_lieu_mau import DANH_SACH_XE_MAU
from presenters.trang_chu_presenter import TrangChuPresenter
from services.parking_service import ParkingService
from views.trang_chu import TrangChu
from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe


APP_STYLE = """
QMessageBox {
    background-color: #FFFFFF;
    color: #050505;
}
QMessageBox QLabel {
    color: #050505;
    background-color: transparent;
}
QMessageBox QPushButton {
    color: #050505;
    background-color: #F3F6FA;
    border: 1px solid #B8C7D9;
    border-radius: 6px;
    padding: 6px 14px;
    min-width: 72px;
}
QMessageBox QPushButton:hover {
    background-color: #E6EDF6;
}
"""


def tao_parking_service_mau():
    bai_xe = QuanLyBaiXe()
    thoi_gian_goc = datetime.now().replace(second=0, microsecond=0)

    for index, (bien_so, loai_xe) in enumerate(DANH_SACH_XE_MAU):
        thoi_gian_vao = thoi_gian_goc - timedelta(minutes=10 * (index + 1))
        xe = XeMay(bien_so, thoi_gian_vao) if loai_xe == "XeMay" else OTo(bien_so, thoi_gian_vao)
        bai_xe.check_in_xe(xe, dua_vao_hang_doi=False)

    return ParkingService(bai_xe)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    view = TrangChu()
    presenter = TrangChuPresenter(view, tao_parking_service_mau())
    presenter.load()

    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
