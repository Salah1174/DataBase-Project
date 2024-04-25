
from main import *  # IMPORTING THE MAIN.PY FILE
import pyodbc

GLOBAL_STATE = 0  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
# NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True
init = False  # NECRESSERY FOR INITITTION OF THE WINDOW.

# tab_Buttons = ['bn_home', ' bn_bug', ' bn_cloud', ' bn_android'] #BUTTONS IN MAIN TAB
# android_buttons = ['bn_android_contact', 'bn_android_game', 'bn_android_clean', 'bn_android_world'] #BUTTONS IN exercises STACKPAGE

# THIS CLASS HOUSES ALL FUNCTION NECESSERY FOR OUR PROGRAMME TO RUN.


def createUser(cursor, Fullname, startDate, endDate, type, Bdate, password, email, address=None, phone=None):
    print(Fullname, startDate, endDate, type,
          Bdate, password, email, address, phone, sep='\n')
    sql_stmt = "INSERT INTO USERS (Username, PasswordHash, Email, U_Address, BirthDate) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql_stmt, (Fullname, password, email, address, Bdate))
    cursor.execute("SELECT @@IDENTITY")
    UserID = cursor.fetchone()[0]
    print(UserID)

    if type == "Trainee":

        sql_stmt = '''INSERT INTO Trainee (StartMembership, EndMembership, UserID)
SELECT ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1
    FROM Trainer
    WHERE Trainer.UserID = ?
)AND NOT EXISTS (
    SELECT 1
    FROM Employee
    WHERE Employee.UserID = ?
)
AND NOT EXISTS (
    SELECT 1
    FROM Trainee
    WHERE Trainee.UserID = ?
);'''

        cursor.execute(sql_stmt, (startDate, endDate,
                       UserID, UserID, UserID, UserID))
    elif type == "Trainer":
        sql_stmt = '''INSERT INTO [Team-5].[dbo].[Trainer] (TrainerRole, UserID)
        SELECT 'Coach', ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM [Team-5].[dbo].[Trainee]
            WHERE [Team-5].[dbo].[Trainee].UserID = ?
        )
        AND NOT EXISTS(
            SELECT 1
            FROM [Team-5].[dbo].[Trainer]
            WHERE [Team-5].[dbo].Trainer.UserID = ?
        )
        AND NOT EXISTS (
            SELECT 1
            FROM [Team-5].[dbo].[Employee]
            WHERE [Team-5].[dbo].[Employee].UserID = ?
        );'''
        cursor.execute(sql_stmt, (UserID, UserID, UserID, UserID))
    elif type == "Employee":
        sql_stmt = '''INSERT INTO Employee (UserID)
        SELECT ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM Trainee
            WHERE Trainee.UserID = ?
        )AND NOT EXISTS(
        SELECT 1 
        FROM Employee
        WHERE Employee.UserID = ?
        )AND NOT EXISTS (
            SELECT 1
            FROM Trainer
            WHERE Trainer.UserID = ?
        );'''
        cursor.execute(sql_stmt, (UserID, UserID, UserID, UserID))


def loginUser(username, password, cursor):
    sql_stmt = f"SELECT * FROM Users WHERE Users.Username = ? AND Users.PasswordHash = ?"
    cursor.execute(sql_stmt, (username, password))
    # print(cursor.fetchall())
    # # print(cursor.fetchall()[0])
    # # print(cursor.fetchall()[1])
    # for data in cursor:
    #     print(data[0][0])

    return cursor.fetchall()


class UIFunction(MainWindow):

    # ----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE
    # INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def initStackTab(self):
        global init
        if init == False:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_login)
            self.ui.lab_tab.setText("Home")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True
    ################################################################################################

    # ------> SETING THE APPLICATION NAME IN OUR CUSTOME MADE TAB, WHERE LABEL NAMED: lab_appname()

    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)
    ################################################################################################

    # ----> MAXIMISE/RESTORE FUNCTION
    # THIS FUNCTION MAXIMISES OUR MAINWINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOEN OVER THE TOPFRMAE.
    # THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            # CHANGE THE MAXIMISE ICON TO RESTOR ICON
            self.ui.bn_max.setIcon(QtGui.QIcon("static/restore.png"))
            # self.ui.frame_drag.hide()  # HIDE DRAG AS NOT NECESSERY
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.bn_max.setToolTip("Maximize")
            # CHANGE BACK TO MAXIMISE ICON
            self.ui.bn_max.setIcon(QtGui.QIcon("static/max.png"))
            self.ui.frame_drag.show()
    ################################################################################################

    # ----> RETURN STATUS MAX OR RESTROE
    # NECESSERY OFR THE MAXIMISE FUNCTION TRO WORK.

    def returStatus():
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # ------> TOODLE MENU FUNCTION
    # THIS FUNCTION TOODLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    # ASLO IT SETS THE ABOUT>HOME AS THE FIRST PAGE.
    # IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMMING BACK TO THE
    # HOME PAGE.

    def toodleMenu(self, maxWidth, clicked):

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if clicked:
            # Reads the current width of the frame
            currentWidth = self.ui.frame_bottom_west.width()
            minWidth = 80  # MINIMUN WITDTH OF THE BOTTOM_WEST FRAME
            if currentWidth == 80:
                extend = maxWidth
                # ----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            else:
                extend = minWidth
                # -----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            # THIS ANIMATION IS RESPONSIBLE FOR THE TOODLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(
                self.ui.frame_bottom_west, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    ################################################################################################

    # -----> DEFAULT ACTION FUNCTION

    def constantFunction(self):
        # -----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(
                    250, lambda: UIFunction.maximize_restore(self))

        # ----> REMOVE NORMAL TITLE BAR
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        # -----> RESIZE USING DRAG                                       THIS CODE TO DRAG AND RESIZE IS IN PROTOPYPE.
        # self.sizegrip = QSizeGrip(self.ui.frame_drag)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        # DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        # -----> MINIMIZE BUTTON FUNCTION
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(
            lambda: UIFunction.maximize_restore(self))

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: self.close())
    ################################################################################################################

    # ----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKEDWIDGET PAGES

    def buttonPressed(self, buttonName, connection, cursor):

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName == 'bn_home' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            print(index)
            if self.ui.frame_bottom_west.width() == 80 and index != 1:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160 and index != 2:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == "submit":
            print(self.ui.stackedWidget.currentWidget())
            print(self.ui.page_login)
            # print(self.ui.stackedWidget.currentWidget())
            fetch = loginUser(self.ui.lineEdit.text(),
                              self.ui.lineEdit_2.text(), cursor)
            # UserID = fetch[0][0]

            if len(fetch) != 0 and self.ui.lineEdit.text() != "" and self.ui.lineEdit_2.text() != "":
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_user.setText(self.ui.lineEdit.text().split()[0])
            else:
                self.errorexec("Incorrect Name or Password",
                               "static/errorAsset 55.png", "Try again")

            # print(index)

        elif buttonName == 'notLogged':
            # print(index)
            self.ui.stackedWidget.setCurrentWidget(self.ui.sign_up)
# def createUser(cursor,Fullname, startDate, endDate, type, Bdate, password, email=None, address=None, phone=None):

        elif buttonName == 'Add_new_user':
            if self.ui.bn_trainee_radio.toggled:
                print("Trainee")
                type = "Trainee"
            elif self.ui.bn_trainer_radio.toggled:
                print("Trainer")
                type = "Trainer"
            elif self.ui.bn_employee_radio.toggled:
                print("Employee")
                type = "Employee"
            name = self.ui.Full_name_field.text()
            start = self.ui.Start_date_field.date().toPython()
            start = start.strftime('%Y-%m-%d')
            end = self.ui.End_date_field.date().toPython()
            end = end.strftime('%Y-%m-%d')
            birth = self.ui.Birth_date_field.date().toPython()
            birth = birth.strftime('%Y-%m-%d')
            password = self.ui.pass_field.text()
            email = self.ui.Email_field.text()
            try:
                if name != "" and password != "" and email != "":
                    createUser(cursor, name, start, end,
                               type, birth, password, email)
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                else:
                    raise Exception
            except:
                self.errorexec("Invalid Input",
                               "static/errorAsset 55.png", "Try again")

        elif buttonName == 'bn_android_contact_save' and self.ui.widget != self.ui.page_login and self.ui.widget != self.ui.sign_up:
            inp = self.ui.line_android_name.text()
            print(inp)

        elif buttonName == 'bn_android_contact_edit' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            inp = self.ui.line_android_name.text()
            print(inp)

        elif buttonName == 'bn_bug_start' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            inp = self.ui.progressBar_bug.text()
            print(inp)

        elif buttonName == 'bn_bug' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("cafeteria")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)
                self.ui.lab_tab.setText("About > cafeteria")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_cloud' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_android)
                self.ui.lab_tab.setText("exercises")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)")
                UIFunction.androidStackPages(self, "page_contact")

            elif self.ui.frame_bottom_west.width() == 160:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(
                    self.ui.page_about_android)
                self.ui.lab_tab.setText("About > exercises")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_android' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.lab_tab.setText("about_us")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(
                    self.ui.page_about_cloud)
                self.ui.lab_tab.setText("About > about_us")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)")

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.
    ########################################################################################################################

    # ----> STACKWIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFOMR THE TASK IN THE STACKED WIDGET PAGE
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.

    def stackPage(self):

        # PAGE_HOME ############# BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_HOME
        self.ui.lab_home_main_hed.setText("Profile")
        self.ui.lab_home_stat_hed.setText("Report")

        # THIS CALLS A SIMPLE FUNCTION LOOPS THROW THE NUMBER FORWARDED BY THE COMBOBOX 'comboBox_bug' AND DISPLAY IN PROGRESS BAR
        # ALONGWITH MOVING THE PROGRESS CHUNK FROM 0 TO 100%

        ######### PAGE about_us #############
        self.ui.bn_cloud_connect.clicked.connect(
            lambda: APFunction.cloudConnect(self))
        self.ui.bn_cloud_clear.clicked.connect(lambda: self.dialogexec(
            "Warning", "Do you want to save the file", "static/errorAsset 55.png", "Cancel", "Save"))
        self.ui.bn_cloud_clear.clicked.connect(
            lambda: APFunction.cloudClear(self))

        # PAGE exercises WIDGET AND ITS STACKANDROID WIDGET PAGES
        self.ui.bn_android_contact.clicked.connect(
            lambda: UIFunction.androidStackPages(self, "page_contact"))
        self.ui.bn_android_game.clicked.connect(
            lambda: UIFunction.androidStackPages(self, "page_game"))
        self.ui.bn_android_clean.clicked.connect(
            lambda: UIFunction.androidStackPages(self, "page_clean"))
        self.ui.bn_android_world.clicked.connect(
            lambda: UIFunction.androidStackPages(self, "page_world"))

        # exercises > PAGE CONTACT >>>>>>>>>>>>>>>>>>>>
        self.ui.bn_android_contact_delete.clicked.connect(lambda: self.dialogexec(
            "Warning", "The Contact Infromtion will be Deleted, Do you want to continue.", "icons/1x/errorAsset 55.png", "Cancel", "Yes"))

        self.ui.bn_android_contact_edit.clicked.connect(
            lambda: APFunction.editable(self))

        self.ui.bn_android_contact_save.clicked.connect(
            lambda: APFunction.saveContact(self))

        # exercises > PAGE GAMEPAD >>>>>>>>>>>>>>>>>>>
        self.ui.textEdit_gamepad.setVerticalScrollBar(
            self.ui.vsb_gamepad)   # SETTING THE TEXT FILED AREA A SCROLL BAR
        self.ui.textEdit_gamepad.setText(
            "Type Here Something, or paste something here")

        # exercises > PAGE CLEAN >>>>>>>>>>>>>>>>>>>>>>
        # NOTHING HERE
        self.ui.horizontalSlider_2.valueChanged.connect(lambda: print(
            # CHECK WEATHER THE SLIDER IS MOVED OR NOT
            "Slider: Horizondal: ", self.ui.horizontalSlider_2.value()))
        # WHEN THE CHECK BOX IS CHECKED IT ECECUTES THE ERROR BOX WITH MESSAGE.
        self.ui.checkBox.stateChanged.connect(lambda: self.errorexec(
            "Happy to Know you liked the UI", "static/smile2Asset 1.png", "Ok"))
        self.ui.checkBox_2.stateChanged.connect(lambda: self.errorexec(
            "Even More Happy to hear this", "static/smileAsset 1.png", "Ok"))

        ########## PAGE: ABOUT HOME #############
        self.ui.text_about_home.setVerticalScrollBar(self.ui.vsb_about_home)
        self.ui.text_about_home.setText("aboutHome")
    ################################################################################################################################

    # -----> FUNCTION TO SHOW CORRESPONDING STACK PAGE WHEN THE exercises BUTTONS ARE PRESSED: CONTACT, GAME, about_us, WORLD
    # SINCE THE exercises PAGE AHS A SUB STACKED WIDGET WIT FOUR MORE BUTTONS, ALL THIS 4 PAGES CONTENT: BUTTONS, TEXT, LABEL E.T.C ARE INITIALIED OVER HERE.

    def androidStackPages(self, page):
        # ------> THIS LINE CLEARS THE BG COLOR OF PREVIOUS TABS
        for each in self.ui.frame_android_menu.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if page == "page_contact":
            self.ui.stackedWidget_android.setCurrentWidget(
                self.ui.page_android_contact)
            self.ui.lab_tab.setText("exercises > Contact")
            self.ui.frame_android_contact.setStyleSheet(
                "background:rgb(91,90,90)")

        elif page == "page_game":
            self.ui.stackedWidget_android.setCurrentWidget(
                self.ui.page_android_game)
            self.ui.lab_tab.setText("exercises > GamePad")
            self.ui.frame_android_game.setStyleSheet(
                "background:rgb(91,90,90)")

        elif page == "page_clean":
            self.ui.stackedWidget_android.setCurrentWidget(
                self.ui.page_android_clean)
            self.ui.lab_tab.setText("exercises > Clean")
            self.ui.frame_android_clean.setStyleSheet(
                "background:rgb(91,90,90)")

        elif page == "page_world":
            self.ui.stackedWidget_android.setCurrentWidget(
                self.ui.page_android_world)
            self.ui.lab_tab.setText("exercises > World")
            self.ui.frame_android_world.setStyleSheet(
                "background:rgb(91,90,90)")

        # ADD A ADDITIONAL ELIF STATEMNT WITH THE SIMILAR CODE UP ABOVE FOR YOUR NEW SUBMENU BUTTON IN THE exercises STACK PAGE.
    ##############################################################################################################


# ------> CLASS WHERE ALL THE ACTION OF TH SOFTWARE IS PERFORMED:
# THIS CLASS IS WHERE THE APPLICATION OF THE UI OR THE BRAINOF THE SOFTWARE GOES
# UNTILL NOW WE SEPCIFIED THE BUTTON CLICKS, SLIDERS, E.T.C WIDGET, WHOSE APPLICATION IS EXPLORED HERE. THOSE FUNCTION WHEN DONE IS
# REDIRECTED TO THIS AREA FOR THE PROCESSING AND THEN THE RESULT ARE EXPOTED.
# REMEMBER THE SOFTWARE UI HAS A FUNCTION WHOSE CODE SHOULD BE HERE
class APFunction():
    # ---> FUNCTION TO CONNECT THE about_us USING ADRESS AND RETURN A ERROR STATEMENT
    def cloudConnect(self):
        self.ui.bn_cloud_clear.setEnabled(False)
        textID = self.ui.line_cloud_id.text()
        textADRESS = self.ui.line_cloud_adress.text()
        if textID == 'asd' and textADRESS == '1234':
            self.ui.line_cloud_adress.setText("")
            self.ui.line_cloud_id.setText("")
            self.ui.line_cloud_proxy.setText("Connection established")
        else:
            self.errorexec("Incorrect Credentials",
                           "static/errorAsset 55.png", "Retry")

    def cloudClear(self):
        self.ui.line_cloud_proxy.setText("")
        self.ui.line_cloud_adress.setText("")
        self.ui.line_cloud_id.setText("")

    # -----> FUNCTION IN ACCOUNT OF CONTACT PAGE IN exercises MENU
    def editable(self):
        self.ui.line_android_name.setEnabled(True)
        self.ui.line_android_adress.setEnabled(True)
        self.ui.line_android_org.setEnabled(True)
        self.ui.line_android_email.setEnabled(True)
        self.ui.line_android_ph.setEnabled(True)

        self.ui.bn_android_contact_save.setEnabled(True)
        self.ui.bn_android_contact_edit.setEnabled(False)
        self.ui.bn_android_contact_share.setEnabled(False)
        self.ui.bn_android_contact_delete.setEnabled(False)

# -----> FUNCTION TO SAVE THE MODOFOED TEXT FIELD
    def saveContact(self):
        self.ui.line_android_name.setEnabled(False)
        self.ui.line_android_adress.setEnabled(False)
        self.ui.line_android_org.setEnabled(False)
        self.ui.line_android_email.setEnabled(False)
        self.ui.line_android_ph.setEnabled(False)

        self.ui.bn_android_contact_save.setEnabled(False)
        self.ui.bn_android_contact_edit.setEnabled(True)
        self.ui.bn_android_contact_share.setEnabled(True)
        self.ui.bn_android_contact_delete.setEnabled(True)
###############################################################################################################################################################
