from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
from views.trang_chu import TrangChu
from presenters.trang_chu_presenter import TrangChuPresenter



app = QApplication(sys.argv)


view = TrangChu()
presenter = TrangChuPresenter(view)

presenter.load()

view.show()
sys.exit(app.exec_())