from PyQt5.QtGui import QColor, QImage, QPainter, QTextDocument, QTextOption


class HoaDonService:
    def tao_html_hoa_don(self, bien_lai):
        xe_ra = bien_lai["xe_ra"]
        so_phut = int(bien_lai["so_phut_gui"])
        loai_xe = "Xe may" if xe_ra.loai_xe == "XeMay" else "O to"
        thanh_tien = f"{bien_lai['tien_gui']:,}".replace(",", ".") + " d"
        return f"""
        <div style="font-family: Arial; width: 460px; padding: 28px; color: #111827;">
            <h2 style="text-align: center; border-bottom: 2px dashed #374151; padding-bottom: 12px; margin: 0; font-size: 24px;">
                HOA DON GUI XE
            </h2>
            <p style="text-align: center; font-size: 14px; color: #4B5563; margin: 12px 0 18px;">
                He thong quan ly bai xe thong minh
            </p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Bien so:</b> {xe_ra.bien_so}</p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Loai xe:</b> {loai_xe}</p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Vi tri do:</b> {bien_lai['ma_vi_tri']}</p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Gio vao:</b> {xe_ra.thoi_gian_vao.strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Gio ra:</b> {bien_lai['thoi_gian_ra'].strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p style="font-size: 16px; margin: 10px 0;"><b>Thoi gian gui:</b> {so_phut // 60} gio {so_phut % 60} phut</p>
            <hr style="border: 1px dashed #D1D5DB; margin: 18px 0;">
            <h3 style="text-align: center; color: #EA580C; font-size: 22px; margin: 0;">
                Thanh tien: {thanh_tien}
            </h3>
        </div>
        """

    def xuat_anh_hoa_don(self, bien_lai, file_path):
        doc = QTextDocument()
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        doc.setDefaultTextOption(text_option)
        doc.setHtml(self.tao_html_hoa_don(bien_lai))
        doc.setTextWidth(520)

        scale = 2
        margin = 24
        width = int(doc.textWidth()) + margin * 2
        height = int(doc.size().height()) + margin * 2
        image = QImage(width * scale, height * scale, QImage.Format_ARGB32)
        image.fill(QColor("white"))

        painter = QPainter(image)
        painter.scale(scale, scale)
        painter.translate(margin, margin)
        doc.drawContents(painter)
        painter.end()
        return image.save(file_path, "PNG")
