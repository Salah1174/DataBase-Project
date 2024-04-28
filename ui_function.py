
import datetime
from main import *  # IMPORTING THE MAIN.PY FILE
import pyodbc

GLOBAL_STATE = 0  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
# NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True
init = False  # NECRESSERY FOR INITITTION OF THE WINDOW.

# tab_Buttons = ['bn_home', ' bn_bug', ' bn_cloud', ' bn_android'] #BUTTONS IN MAIN TAB
# android_buttons = ['bn_android_contact', 'bn_android_game', 'bn_android_clean', 'bn_android_world'] #BUTTONS IN exercises STACKPAGE

USERNAME = ""
PASSWORD = ""
ID = -1


def createUser(cursor, Fullname, startDate, endDate, type1, Bdate, password, email, address=None, phone=None):
    print(Fullname, startDate, endDate, type1,
          Bdate, password, email, address, phone, sep='\n')
    sql_stmt = "INSERT INTO USERS (Username, PasswordHash, Email, U_Address, BirthDate) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql_stmt, (Fullname, password, email, address, Bdate))
    cursor.execute("SELECT @@IDENTITY")
    UserID = cursor.fetchone()[0]
    print(UserID)

    if type1 == "Trainee":

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
    elif type1 == "Trainer":
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
    elif type1 == "Employee":
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
    sql_stmt = f"SELECT * FROM Users WHERE Users.Username = ? AND Users.PasswordHash = ? COLLATE Latin1_General_CS_AS;"
    cursor.execute(sql_stmt, (username, password))
    return cursor.fetchall()


def getUserinfo(self, cursor):
    if self.ui.Full_name_field.text() == "":
        return loginUser(self.ui.lineEdit.text(),
                         self.ui.lineEdit_2.text(), cursor)
    else:
        return loginUser(self.ui.Full_name_field.text(),
                         self.ui.pass_field.text(), cursor)


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

    def returStatus():
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

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
            fetch = loginUser(self.ui.lineEdit.text(),
                              self.ui.lineEdit_2.text(), cursor)
            if len(fetch) != 0 and self.ui.lineEdit.text() != "" and self.ui.lineEdit_2.text() != "":
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                username = self.ui.lineEdit.text().split()[0]
                email = fetch[0][3]
                Bdate = fetch[0][5]
                age = fetch[0][8]
                id = fetch[0][0]
                sql_stmt = f"SELECT * FROM Trainee WHERE Trainee.UserID = ?;"
                type1 = "Trainee"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                if len(traineeinfo) == 0:
                    sql_stmt = f"SELECT * FROM Trainer WHERE Trainer.UserID = ?;"
                    traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()

                    type1 = "Trainer"
                if len(traineeinfo) == 0:
                    sql_stmt = f"SELECT * FROM Employee WHERE Employee.UserID = ?;"
                    traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                    type1 = "Employee"
                if type1 != "Employee":
                    self.ui.bn_android.setVisible(False)
                typid = traineeinfo[0][0]
                start = traineeinfo[0][1]
                end = traineeinfo[0][2]
                self.ui.lab_user.setText(str(id))
                height = "N/A"
                weight = "N/A"
                self.ui.lab_home_stat_disc.setText(
                    f"<html><head/><body><p><span style=\" color:#ffffff;\">ID: {id}<br/>{type1}id: {typid}<br />Name: {username}<br/>Email: {email}<br/>Age:{age}<br/>Start Date: {start}<br/>End Date: {end}<br/>Birth Date: {Bdate}<br/>Height: {height}<br/>Weight: {weight}</span></p></body></html>")
            else:
                self.errorexec("Incorrect Name or Password",
                               "static/errorAsset 55.png", "Try again")

        elif buttonName == 'notLogged':
            self.ui.stackedWidget.setCurrentWidget(self.ui.sign_up)

        elif buttonName == 'Add_new_user':
            if self.ui.bn_trainee_radio.toggled:
                print("Trainee")
                type1 = "Trainee"
            elif self.ui.bn_trainer_radio.toggled:
                print("Trainer")
                type1 = "Trainer"
            elif self.ui.bn_employee_radio.toggled:
                print("Employee")
                type1 = "Employee"
            username = self.ui.Full_name_field.text()
            start = self.ui.Start_date_field.date().toPython()
            start = start.strftime('%Y-%m-%d')
            end = self.ui.End_date_field.date().toPython()
            end = end.strftime('%Y-%m-%d')
            Bdate = self.ui.Birth_date_field.date().toPython()
            age = datetime.datetime.now().year - Bdate.year
            Bdate = Bdate.strftime('%Y-%m-%d')
            password = self.ui.pass_field.text()
            email = self.ui.Email_field.text()
            if username != "" and password != "" and email != "":
                createUser(cursor, username, start, end,
                           type1, Bdate, password, email)
                try:
                    print(username.split()[0])
                    sql_stmt = f"SELECT * FROM Users WHERE Users.Username = ? AND Users.PasswordHash = ? COLLATE Latin1_General_CS_AS;"
                    id = cursor.execute(
                        sql_stmt, (username, password)).fetchall()[0][0]
                except pyodbc.Error as e:
                    print("Error", e)
                self.ui.lab_user.setText(str(id))
                # self.ui.lab_user.setText(name.split()[0])
                # member = cursor.execute(
                #     "Select type1 from Membership where TraineeID = ?", (id)).fetchall()[0][4]
                self.ui.lab_home_stat_disc.setText(
                    f"<html><head/><body><p><span style=\" color:#ffffff;\">ID: {id}<br/>Name: {username}<br/>Email: {email}<br/>Age:{age}<br/>Birth Date: {Bdate}<br/>Start Date: {start}<br/>End Date: {end}<br/>MemberShip type: N/A </span></p></body></html>")
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

            else:
                #     raise Exception
                self.errorexec("Invalid Input",
                               "static/errorAsset 55.png", "Try again")
        elif buttonName == 'bn_android_contact_edit':
            sql_stmt = f"SELECT * FROM Trainee WHERE Trainee.UserID = ?;"
            id = getUserinfo(self, cursor)[0][0]
            traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
            type1 = "Trainee"
            if len(traineeinfo) == 0:
                sql_stmt = f"SELECT * FROM Trainer WHERE Trainer.UserID = ?;"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                type1 = "Trainer"
            if len(traineeinfo) == 0:
                sql_stmt = f"SELECT * FROM Employee WHERE Employee.UserID = ?;"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                type1 = "Employee"
            self.ui.bn_android_contact_save.setEnabled(True)
            self.ui.bn_android_contact_edit.setEnabled(False)
            self.ui.line_android_name.setEnabled(True)
            self.ui.line_android_ph.setEnabled(True)
            self.ui.line_android_email.setEnabled(True)
            self.ui.line_android_height.setEnabled(True)
            self.ui.line_android_adress.setEnabled(True)
            self.ui.line_android_weight.setEnabled(True)
            if type1 == "Employee":
                x = True
                y = True
            elif type1 == "Trainer":
                x = False
                y = False
            elif type1 == "Trainee":
                x = False
                y = True
            self.ui.line_android_role.setEnabled(x)
            self.ui.line_android_membership.setEnabled(y)

        elif buttonName == 'bn_android_contact_save':
            sql_stmt = f"SELECT * FROM Trainee WHERE Trainee.UserID = ?;"
            id = getUserinfo(self, cursor)[0][0]
            traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
            id = traineeinfo[0][3]
            type1 = "Trainee"
            if len(traineeinfo) == 0:
                sql_stmt = f"SELECT * FROM Trainer WHERE Trainer.UserID = ?;"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                type1 = "Trainer"
            if len(traineeinfo) == 0:
                sql_stmt = f"SELECT * FROM Employee WHERE Employee.UserID = ?;"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                type1 = "Employee"

            self.ui.bn_android_contact_save.setEnabled(False)
            self.ui.bn_android_contact_edit.setEnabled(True)
            self.ui.line_android_name.setEnabled(False)
            self.ui.line_android_ph.setEnabled(False)
            self.ui.line_android_email.setEnabled(False)
            self.ui.line_android_adress.setEnabled(False)
            self.ui.line_android_role.setEnabled(False)
            self.ui.line_android_membership.setEnabled(False)
            self.ui.line_android_adress.setEnabled(False)
            self.ui.line_android_weight.setEnabled(False)

            if self.ui.Full_name_field.text() == "":
                username = self.ui.lineEdit.text()
                password = self.ui.lineEdit_2.text()
                id = loginUser(self.ui.lineEdit.text(),
                               self.ui.lineEdit_2.text(), cursor)[0][0]
            else:
                username = self.ui.Full_name_field.text()
                password = self.ui.pass_field.text()
                sql_stmt = f"SELECT * FROM Users WHERE Users.Username = ? AND Users.PasswordHash = ? COLLATE Latin1_General_CS_AS;"
                id = cursor.execute(
                    sql_stmt, (username, password)).fetchall()[0][0]
            username = self.ui.line_android_name.text()
            phone = self.ui.line_android_adress.text()
            address = self.ui.line_android_ph.text()
            email = self.ui.line_android_email.text()
            sql_stmt = "exec edituserinfo ?,?,?,?,?,?"
            cursor.execute(
                sql_stmt, (id, password, username, phone, email, address))
        elif buttonName == 'bn_bug_start' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            inp = self.ui.progressBar_bug.text()
            print(type(inp))
            inp = int(inp)
            print(type(inp))
            sql_stmt = "exec getUserInfo ?"
            cursor.execute(sql_stmt, (inp))
            fetch1 = cursor.fetchall()

            self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)

            if (len(fetch1) == 0):
                self.ui.lab_bug_main_hed.setText(
                    "........................Not Found")
            else:
                self.ui.lab_bug_main_hed.setText(
                    "........................................"+str(inp))
                self.ui.lab_bug_main_disc.setText(f"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  f"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  f"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">User Found!<br /></p>\n"
                                                  f"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-ID: {
                                                      fetch1[0][0]}<br /></p>\n"
                                                  f"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"-Name:{
                                                      fetch1[0][1]}<br /></p>\n"
                                                  f"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Proper Form is Crucial:<br /></p>\n"
                                                  f"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
                                                  f"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                  f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>")

     ################################################################################
            # if len(fetch.fetchall()) != 0:
            #     self.ui.searchresults.setText("Found")
            #     self.ui.searchresults.setText(str(fetch.fetchall()[0]))
            print(inp)

        elif buttonName == 'bn_bug' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("cafeteria")
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_cloud' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                fetch = loginUser(self.ui.lineEdit.text(),
                                  self.ui.lineEdit_2.text(), cursor)
                if (self.ui.lineEdit.text() == ""):
                    username = self.ui.Full_name_field.text().split()[0]
                    password = self.ui.pass_field.text()
                else:
                    username = self.ui.lineEdit.text()
                    password = self.ui.lineEdit_2.text()
                email = cursor.execute("select email from Users where Username=? and PasswordHash=?", (
                    username, password)).fetchall()[0][0]
                print(email)
                self.ui.line_android_name.setText(username)
                self.ui.line_android_adress.setText("")
                self.ui.line_android_ph.setText("")
                self.ui.line_android_email.setText(str(email))
                self.ui.stackedWidget.setCurrentWidget(
                    self.ui.page_android)
                self.ui.lab_tab.setText("Users")
                self.ui.frame_cloud.setStyleSheet(
                    "background:rgb(91,90,90)")
                UIFunction.androidStackPages(self, "page_contact")

        elif buttonName == 'bn_android' and self.ui.stackedWidget.currentWidget() != self.ui.page_login and self.ui.stackedWidget.currentWidget() != self.ui.sign_up:
            if self.ui.frame_bottom_west.width() == 80:
                id = getUserinfo(self, cursor)[0][0]
                sql_stmt = f"SELECT * FROM Trainee WHERE Trainee.UserID = ?;"
                traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                type1 = "Trainee"
                if len(traineeinfo) == 0:
                    sql_stmt = f"SELECT * FROM Trainer WHERE Trainer.UserID = ?;"
                    traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                    type1 = "Trainer"
                if len(traineeinfo) == 0:
                    sql_stmt = f"SELECT * FROM Employee WHERE Employee.UserID = ?;"
                    traineeinfo = cursor.execute(sql_stmt, (id)).fetchall()
                    type1 = "Employee"
                if type1 == "Employee":
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                    self.ui.lab_tab.setText("about you")
                    self.ui.frame_android.setStyleSheet(
                        "background:rgb(91,90,90)")
                elif type1 == "Trainer":
                    self.ui.line_android_role.setModelColumn(0)
                    self.ui.line_android_membership.setModelColumn(4)
                elif type1 == "Trainee":
                    self.ui.line_android_role.setModelColumn(5)
                    self.ui.line_android_membership.setModelColumn(4)

        elif buttonName == 'bn_cloud_connect':
            name = self.ui.line_cloud_id.text()
            password = self.ui.line_cloud_adress.text()
            email = self.ui.line_cloud_proxy.text()
            birth = self.ui.Birth_date_field_2.text()
            start = self.ui.Start_Date_field_2.text()
            end = self.ui.End_Date_field_2.text()
            if self.ui.bn_trainee_radio_2.toggled:
                type1 = "Trainee"
            elif self.ui.bn_trainer_radio_2.toggled:
                type1 = "Trainer"
            elif self.ui.bn_Employee_radio_2.toggled:
                type1 = "Employee"
            if name != "" and password != "" and email != "":
                createUser(cursor, name, start, end,
                           type1, birth, password, email)
                try:
                    print(name.split()[0])
                    sql_stmt = f"SELECT * FROM Users WHERE Users.Username = ? AND Users.PasswordHash = ? COLLATE Latin1_General_CS_AS;"
                    id = cursor.execute(
                        sql_stmt, (name, password)).fetchall()[0][0]
                    self.errorexec("User Created Successfully",
                                   "static/smile2Asset 1.png", "OK")
                    APFunction.cloudClear(self)
                except:
                    print("Error")
            else:
                # raise Exception
                self.errorexec("Invalid Input",
                               "static/errorAsset 55.png", "Try again")

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.
    ########################################################################################################################

    def stackPage(self):

        # PAGE_HOME ############# BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_HOME
        self.ui.lab_home_main_hed.setText("Profile")
        self.ui.lab_home_main_hed.setStyleSheet("color: rgb(255, 255, 255);")
        self.ui.lab_home_stat_hed.setText("Report")
        self.ui.lab_home_main_disc.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "</style></head><body style=\" font-family:\'Segoe UI\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome to our CrossFit community!<br /> Here's some personalized advice to help you maximize your workouts and maintain optimal health:</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Variety is Key:<br /> Mix up your workouts regularly to challenge different muscle groups and prevent plateaus.<br /> Incorporate a combination of strength training, HIIT, cardio, and mobility work for a well-rounded fitness regimen.</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"- Functional Movements:<br /> Focus on exercises that mimic everyday movements to improve your overall strength and agility.<br /> Squats, deadlifts, push-ups, and pull-ups are great examples of functional exercises that translate into real-life activities.</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Proper Form is Crucial:<br /> Prioritize technique over intensity to avoid injuries.<br /> Start with lighter weights and gradually increase as you master the movements.<br /> Don't hesitate to ask a coach for guidance or feedback on your form.:</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Listen to Your Body: Pay attention to any signs of fatigue or discomfort during workouts. Rest when needed and prioritize recovery to prevent overtraining and burnout. Adequate sleep, hydration, and nutrition are essential for supporting your fitness goals.</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Nutrition Matters: Fuel your body with whole, nutrient-dense foods to support your training and recovery. Aim for a balanced diet rich in lean protein, complex carbohydrates, healthy fats, and plenty of fruits and vegetables. Consider consulting with a nutritionist for personalized dietary guidance.</p></body></html>")

        ######### PAGE about_us #############

        # PAGE exercises WIDGET AND ITS STACKANDROID WIDGET PAGES
        # self.ui.bn_android_contact.clicked.connect(
        #     lambda: UIFunction.androidStackPages(self, "page_contact"))
        # self.ui.bn_android_game.clicked.connect(
        #     lambda: UIFunction.androidStackPages(self, "page_game"))
        # self.ui.bn_android_clean.clicked.connect(
        #     lambda: UIFunction.androidStackPages(self, "page_clean"))
        # self.ui.bn_android_world.clicked.connect(
        #     lambda: UIFunction.androidStackPages(self, "page_world"))

        # # exercises > PAGE CONTACT >>>>>>>>>>>>>>>>>>>>
        # self.ui.bn_android_contact_delete.clicked.connect(lambda: self.dialogexec(
        #     "Warning", "The Contact Infromtion will be Deleted, Do you want to continue.", "static/errorAsset 55.png", "Cancel", "Yes"))

        # self.ui.bn_android_contact_edit.clicked.connect(
        #     lambda: APFunction.editable(self))

        # self.ui.bn_android_contact_save.clicked.connect(
        #     lambda: APFunction.saveContact(self))

        # exercises > PAGE GAMEPAD >>>>>>>>>>>>>>>>>>>
        self.ui.textEdit_gamepad.setVerticalScrollBar(
            self.ui.vsb_gamepad)   # SETTING THE TEXT FILED AREA A SCROLL BAR
        self.ui.textEdit_gamepad.setText(
            "type1 Here Something, or paste something here")

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


class APFunction():
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
