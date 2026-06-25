import csv
import json
import os


DATA_DIR = os.path.dirname(__file__)
LICH_SU_CSV = os.path.join(DATA_DIR, "lich_su_gui_xe.csv")
LICH_SU_JSON = os.path.join(DATA_DIR, "lich_su_gui_xe.json")
CAC_COT_LICH_SU = [
    "bien_so",
    "loai_xe",
    "vi_tri",
    "gio_vao",
    "gio_ra",
    "so_phut_gui",
    "thanh_tien",
]


def _tao_thu_muc_neu_chua_co():
    os.makedirs(DATA_DIR, exist_ok=True)


def doc_lich_su_csv(duong_dan=LICH_SU_CSV):
    if not os.path.exists(duong_dan):
        return []

    with open(duong_dan, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def ghi_them_lich_su_csv(ban_ghi, duong_dan=LICH_SU_CSV):
    _tao_thu_muc_neu_chua_co()
    can_ghi_header = not os.path.exists(duong_dan) or os.path.getsize(duong_dan) == 0
    with open(duong_dan, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CAC_COT_LICH_SU)
        if can_ghi_header:
            writer.writeheader()
        writer.writerow({cot: ban_ghi.get(cot, "") for cot in CAC_COT_LICH_SU})


def doc_lich_su_json(duong_dan=LICH_SU_JSON):
    if not os.path.exists(duong_dan):
        return []

    with open(duong_dan, "r", encoding="utf-8") as file:
        try:
            du_lieu = json.load(file)
        except json.JSONDecodeError:
            return []
    return du_lieu if isinstance(du_lieu, list) else []


def ghi_lich_su_json(danh_sach_ban_ghi, duong_dan=LICH_SU_JSON):
    _tao_thu_muc_neu_chua_co()
    with open(duong_dan, "w", encoding="utf-8") as file:
        json.dump(danh_sach_ban_ghi, file, ensure_ascii=False, indent=2)


def luu_ban_ghi_lich_su(ban_ghi):
    ghi_them_lich_su_csv(ban_ghi)
    lich_su_json = doc_lich_su_json()
    lich_su_json.append(ban_ghi)
    ghi_lich_su_json(lich_su_json)
