def quick_sort(danh_sach, key, reverse=True):
    if len(danh_sach) <= 1:
        return list(danh_sach)

    pivot = danh_sach[len(danh_sach) // 2]
    gia_tri_pivot = _lay_gia_tri(pivot, key)
    nho_hon = []
    bang = []
    lon_hon = []

    for item in danh_sach:
        gia_tri = _lay_gia_tri(item, key)
        if gia_tri < gia_tri_pivot:
            nho_hon.append(item)
        elif gia_tri > gia_tri_pivot:
            lon_hon.append(item)
        else:
            bang.append(item)

    if reverse:
        return quick_sort(lon_hon, key, reverse) + bang + quick_sort(nho_hon, key, reverse)
    return quick_sort(nho_hon, key, reverse) + bang + quick_sort(lon_hon, key, reverse)


def _lay_gia_tri(item, key):
    if callable(key):
        return key(item)
    if isinstance(item, dict):
        return item.get(key, 0)
    return getattr(item, key)


def sap_xep_theo_thoi_gian_gui(danh_sach_lich_su):
    return quick_sort(
        danh_sach_lich_su,
        lambda ban_ghi: int(ban_ghi.get("so_phut_gui", 0) or 0),
        reverse=True,
    )


def sap_xep_theo_doanh_thu(danh_sach_lich_su):
    return quick_sort(
        danh_sach_lich_su,
        lambda ban_ghi: int(ban_ghi.get("thanh_tien", 0) or 0),
        reverse=True,
    )
