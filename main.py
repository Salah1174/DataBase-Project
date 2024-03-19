import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon

from Home import Ui_MainWindow
# from ui_main import Ui_MainWindow as ui_main
from ui_function import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.username = self.ui.lineEdit
        self.password = self.ui.lineEdit_2
        self.username.addAction(
            QIcon("static/businessman.png"), QLineEdit.ActionPosition.LeadingPosition)
        self.password.addAction(
            QIcon("static/padlock.png"), QLineEdit.ActionPosition.LeadingPosition)


class HomeWindow(QMainWindow):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
