# IMPORTING ALL THE NECESSERY PYSIDE6 MODULES FOR OUR APPLICATION.
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                           QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
import pyodbc
from ui_main1 import Ui_MainWindow
from ui_dialog import Ui_Dialog  # DIALOGBOX WINDOW GENERATED BY THE ABOVEW SAME
from ui_error import Ui_Error  # ERRORBOX WINDOW GENERATED BY THE ABOVE SAME
from ui_function import *


class dialogUi(QDialog):
    def __init__(self, parent=None):

        super(dialogUi, self).__init__(parent)
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        # REMOVING WINDOWS TOP BAR AND MAKING IT FRAMELESS (AS WE HAVE AMDE A CUSTOME FRAME IN THE WINDOW ITSELF)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # MAKING THE WINDOW TRANSPARENT SO THAT TO GET A TRUE FLAT UI
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.d.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.d.bn_close.clicked.connect(lambda: self.close())

        # -----> THIS FUNCTION WILL CHECKT WEATHER THE BUTRTON ON THE DIALOGBOX IS CLICKED, AND IF SO DIRECTS TO THE FUNCTINON : diag_return()
        self.d.bn_east.clicked.connect(lambda: self.close())
        self.d.bn_west.clicked.connect(lambda: self.close())
        ##############################################################################################

        def movedialogWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.d.frame_top.mouseMoveEvent = movedialogWindow
        ################
    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    #################################################################################################

    def dialogConstrict(self, heading, message, icon, btn1, btn2):
        self.d.lab_heading.setText(heading)
        self.d.lab_message.setText(message)
        self.d.bn_east.setText(btn2)
        self.d.bn_west.setText(btn1)
        pixmap = QtGui.QPixmap(icon)
        self.d.lab_icon.setPixmap(pixmap)
    ##################################################################################################


class errorUi(QDialog):
    def __init__(self, parent=None):

        super(errorUi, self).__init__(parent)
        self.e = Ui_Error()
        self.e.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.e.bn_ok.clicked.connect(lambda: self.close())

        self.dragPos = self.pos()  # INITIAL POSOTION OF THE ERRORBOX

        def moveWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.e.frame_top.mouseMoveEvent = moveWindow
        ################

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
#############################################

    def errorConstrict(self, heading, icon, btnOk):
        self.e.lab_heading.setText(heading)
        self.e.bn_ok.setText(btnOk)
        pixmap2 = QtGui.QPixmap(icon)
        self.e.lab_icon.setPixmap(pixmap2)


# OUR APPLICATION MAIN WINDOW :
# -----> MAIN APPLICATION CLASS
class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ----> SET WINDOW TITLE AND ICON
        applicationName = "CrossFit Team-5"
        ############################################################
        self.setWindowTitle(applicationName)
        ############################################################
        UIFunction.labelTitle(self, applicationName)
        ############################################################
        UIFunction.initStackTab(self)
        ############################################################
        UIFunction.constantFunction(self)
        #############################################################
        self.ui.bn_home.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_home', connection, cursor))
        self.ui.submit.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'submit', connection, cursor))
        self.ui.bn_bug.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_bug', connection, cursor))
        self.ui.bn_cloud.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_cloud', connection, cursor))
        self.ui.bn_android.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_android', connection, cursor))
        self.ui.Add_new_user.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'Add_new_user', connection, cursor))
        self.ui.notLogged.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'notLogged', connection, cursor))
        self.ui.bn_android_contact_edit.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_android_contact_edit', connection, cursor))
        self.ui.bn_android_contact_save.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_android_contact_save', connection, cursor))
        self.ui.Add_new_Report.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'Add_new_Report', connection, cursor))
        #############################################################
        UIFunction.stackPage(self)
        #############################################################
        self.error = errorUi()
        #############################################################

        #############################################################

        inp = self.ui.line_android_name.text()
        print(inp)
        # self.ui.bn_android_contact_save.clicked.connect(
        #     lambda: UIFunction.buttonPressed(self, 'bn_android_contact_save'))
        # self.ui.bn_android_contact_edit.clicked.connect(
        #     lambda: UIFunction.buttonPressed(self, 'bn_android_contact_edit'))
        self.ui.bn_bug_start.clicked.connect(
            lambda: UIFunction.buttonPressed(self, 'bn_bug_start', connection, cursor))
        self.ui.bn_cloud_connect.clicked.connect(
            lambda: UIFunction.buttonPressed(self, "bn_cloud_connect", connection, cursor))
        self.ui.bn_cloud_clear.clicked.connect(
            lambda: APFunction.cloudClear(self))
        # self.ui.bn_android_contact_save.clicked.connect(
        #     lambda: UIFunction.buttonPressed(self, 'bn_android_contact_save'))
        # self.ui.bn_android_contact_save.clicked.connect(
        #     lambda: UIFunction.buttonPressed(self, 'bn_android_contact_save'))
        # PERFORM THE SAME CODE FOR THE: OBJECT NAME: 'line_android_adress', 'line_android_eamil', 'line_android_ph', 'line_android_org'

        self.dragPos = self.pos()

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunction.returStatus() == 1:
                UIFunction.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_appname.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    #############################################################

    def dialogexec(self, heading, message, icon, btn1, btn2):
        dialogUi.dialogConstrict(self.diag, heading, message, icon, btn1, btn2)
        self.diag.exec_()
    #############################################################

    def errorexec(self, heading, icon, btnOk):
        errorUi.errorConstrict(self.error, heading, icon, btnOk)
        self.error.exec_()
    ##############################################################


if __name__ == "__main__":
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};' +
                                    'Server=LAPTOP-019RIHG4;' +
                                    'Database=CrossFit;' +
                                    'Trusted_Connection=True;')

        print("Connection Established")
        connection.autocommit = True
        cursor = connection.cursor()
    except pyodbc.Error as e:
        print("Connection Failed", e)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

############################################################################################################################################################
