from main import *  # IMPORTING THE MAIN.PY FILE

# from about import *

GLOBAL_STATE = 0  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
# NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True
init = False  # NECRESSERY FOR INITITTION OF THE WINDOW.


class UIFunction(MainWindow):
    def initStackTab(self):
        global init
        if init == False:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.lab_tab.setText("Home")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True

    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName == 'bn_home':
            if self.ui.frame_bottom_west.width() == 80 and index != 0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160 and index != 1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_bug':
            if self.ui.frame_bottom_west.width() == 80 and index != 5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("Bug")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160 and index != 4:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)
                self.ui.lab_tab.setText("About > Bug")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_bug.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_android':
            if self.ui.frame_bottom_west.width() == 80 and index != 7:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_android)
                self.ui.lab_tab.setText("Android")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)")
                UIFunction.androidStackPages(self, "page_contact")

            elif self.ui.frame_bottom_west.width() == 160 and index != 3:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(
                    self.ui.page_about_android)
                self.ui.lab_tab.setText("About > Android")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_android.setStyleSheet("background:rgb(91,90,90)")

        elif buttonName == 'bn_cloud':
            if self.ui.frame_bottom_west.width() == 80 and index != 6:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.lab_tab.setText("Cloud")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)")

            elif self.ui.frame_bottom_west.width() == 160 and index != 2:   # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(
                    self.ui.page_about_cloud)
                self.ui.lab_tab.setText("About > Cloud")
                # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                self.ui.frame_cloud.setStyleSheet("background:rgb(91,90,90)")

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.
    ########################################################################################################################
