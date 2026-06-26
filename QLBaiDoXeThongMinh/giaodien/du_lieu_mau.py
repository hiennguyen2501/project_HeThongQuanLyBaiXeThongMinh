import os
import sys
from datetime import datetime, timedelta


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from doituong.loai_xe import OTo, XeMay
from giaodien.services.parking_service import ParkingService
from xulyhethong.quan_ly_bai_xe import QuanLyBaiXe


def tao_parking_service_mau():
    bai_xe = QuanLyBaiXe()
    thoi_gian_goc = datetime.now().replace(second=0, microsecond=0)
    so_o_moi_loai = (bai_xe.so_hang // 2) * bai_xe.so_cot

    for index in range(so_o_moi_loai):
        bien_so = f"59A1-{10001 + index}"
        thoi_gian_vao = thoi_gian_goc - timedelta(minutes=15 * (index + 1))
        bai_xe.check_in_xe(XeMay(bien_so, thoi_gian_vao), dua_vao_hang_doi=False)

    for index in range(so_o_moi_loai):
        bien_so = f"30A-{20001 + index}"
        thoi_gian_vao = thoi_gian_goc - timedelta(minutes=20 * (index + 1))
        bai_xe.check_in_xe(OTo(bien_so, thoi_gian_vao), dua_vao_hang_doi=False)

    return ParkingService(bai_xe)
