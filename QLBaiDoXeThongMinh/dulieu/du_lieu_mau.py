from datetime import datetime

from doituong.loai_xe import OTo, XeMay


def _hom_nay_luc(gio, phut=0):
    return datetime.now().replace(hour=gio, minute=phut, second=0, microsecond=0)


def _tao_xe_may(bat_dau, ket_thuc, gio_bat_dau=6):
    danh_sach = []
    for index in range(bat_dau, ket_thuc + 1):
        tong_phut = (index - bat_dau) * 7
        gio = gio_bat_dau + tong_phut // 60
        phut = tong_phut % 60
        danh_sach.append(
            XeMay(f"59A1-{10000 + index}", thoi_gian_vao=_hom_nay_luc(gio, phut))
        )
    return danh_sach


def _tao_o_to(bat_dau, ket_thuc, gio_bat_dau=6):
    danh_sach = []
    for index in range(bat_dau, ket_thuc + 1):
        tong_phut = (index - bat_dau) * 9
        gio = gio_bat_dau + tong_phut // 60
        phut = tong_phut % 60
        danh_sach.append(
            OTo(f"30A-{50000 + index}", thoi_gian_vao=_hom_nay_luc(gio, phut))
        )
    return danh_sach


def tao_xe_dang_gui_mau():
    return _tao_xe_may(1, 48) + _tao_o_to(1, 48)


def tao_xe_cho_mau():
    return _tao_xe_may(101, 106, gio_bat_dau=12) + _tao_o_to(101, 106, gio_bat_dau=12)


def tao_lich_su_xe_ra_mau():
    mau = [
        ("59A1-20001", "Xe may", "A01", 5, 50, 7, 5, 5000),
        ("59B1-20002", "Xe may", "A02", 6, 0, 7, 20, 5000),
        ("59C1-20003", "Xe may", "A03", 6, 10, 7, 45, 5000),
        ("59D1-20004", "Xe may", "A04", 6, 20, 8, 10, 5000),
        ("59E1-20005", "Xe may", "A05", 6, 30, 8, 35, 5000),
        ("59F1-20006", "Xe may", "A06", 6, 40, 9, 0, 5000),
        ("59G1-20007", "Xe may", "A07", 6, 50, 9, 25, 5000),
        ("59H1-20008", "Xe may", "A08", 7, 0, 9, 50, 5000),
        ("30A-60001", "O to", "A01", 5, 45, 7, 0, 35000),
        ("30B-60002", "O to", "A02", 6, 5, 7, 40, 35000),
        ("30C-60003", "O to", "A03", 6, 25, 8, 30, 50000),
        ("30D-60004", "O to", "A04", 6, 45, 9, 10, 50000),
        ("30E-60005", "O to", "A05", 7, 5, 10, 0, 65000),
        ("30F-60006", "O to", "A06", 7, 25, 10, 40, 65000),
        ("30G-60007", "O to", "A07", 7, 45, 11, 20, 80000),
        ("30H-60008", "O to", "A08", 8, 5, 12, 0, 80000),
        ("30K-60009", "O to", "A09", 8, 25, 12, 45, 95000),
        ("30L-60010", "O to", "A10", 8, 45, 13, 30, 95000),
        ("30M-60011", "O to", "A11", 9, 5, 14, 15, 110000),
        ("30N-60012", "O to", "A12", 9, 25, 15, 0, 110000),
    ]

    lich_su = []
    for bien_so, loai_xe, vi_tri, gio_vao, phut_vao, gio_ra, phut_ra, thanh_tien in mau:
        thoi_gian_vao = _hom_nay_luc(gio_vao, phut_vao)
        thoi_gian_ra = _hom_nay_luc(gio_ra, phut_ra)
        so_phut_gui = max(1, int((thoi_gian_ra - thoi_gian_vao).total_seconds() // 60))
        lich_su.append({
            "bien_so": bien_so,
            "loai_xe": loai_xe,
            "vi_tri": vi_tri,
            "gio_vao": thoi_gian_vao.isoformat(timespec="seconds"),
            "gio_ra": thoi_gian_ra.isoformat(timespec="seconds"),
            "so_phut_gui": so_phut_gui,
            "thanh_tien": thanh_tien,
        })
    return lich_su
