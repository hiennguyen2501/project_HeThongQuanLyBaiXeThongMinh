from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
from views.trang_chu import TrangChu
from presenters.trang_chu_presenter import TrangChuPresenter



app = QApplication(sys.argv)
app.setStyleSheet("""
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
""")


view = TrangChu()
presenter = TrangChuPresenter(view)

presenter.load()

view.show()
sys.exit(app.exec_())
