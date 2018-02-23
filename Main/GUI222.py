from PyQt4 import QtCore, QtGui
import sys
import os, webbrowser
import shutil
import numpy as np
from save_data import main

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(250, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(250, 300))
        MainWindow.setMaximumSize(QtCore.QSize(250, 300))


        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        def start_func(self):
            print('start')
            #main() #crashes
            #os.system("save_data.py") #crashes

        def stop_func(self):
            print('stop')


        def send_func(self):
            print('send')


        def gitHub_func(self):
            webbrowser.open('https://github.com/Setti7/Stardew-Valley-Fishing-Bot')

        def del_last_data(self):

            choice = QtGui.QMessageBox.question(MainWindow, "Warning!", "Are you sure you want to delete the data from your last fishing?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if choice == QtGui.QMessageBox.Yes:

                try:

                    file_name = 'Data\\training_data.npy'
                    frames_file = 'Data\\frames.npy'

                    training_data = list(np.load(file_name))
                    frames = list(np.load(frames_file))

                    before_score = sum(frames)

                    print(len(frames))
                    print(frames)
                    print(len(training_data))

                    if len(frames) == 1: #if there is only 1 fishing session, delete all

                        data_folder = os.getcwd()
                        data_folder_path = os.path.join(data_folder, 'Data')

                        for file in os.listdir(data_folder_path):

                            file_path = os.path.join(data_folder_path, file)
                            print(file, ' removed')
                            os.remove(file_path)

                        QtGui.QMessageBox.information(MainWindow, "Success", 'Your last data was deleted...')

                    else:

                        del training_data[-frames[-1]:]
                        del frames[-1]

                        np.save(file_name, training_data)
                        np.save(frames_file, frames)

                        after_score = sum(frames)

                        string = 'Last data was removed successfully!\n\n\tScore before deletion:\t' + str(before_score) + '\n\tYour score now:\t' + str(after_score)
                        print(string)
                        QtGui.QMessageBox.information(MainWindow, "Success", string)

                except Exception as e:
                    print(e)
                    QtGui.QMessageBox.information(MainWindow, "Oops!", "Could not delete the Data")


        def del_data(self):

            choice = QtGui.QMessageBox.question(MainWindow, "Warning!", "Are you sure you want to delete all data you gathered? Remember: you can delete just the last one multiple times!", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if choice == QtGui.QMessageBox.Yes:

                try:
                    data_folder = os.getcwd()
                    data_folder_path = os.path.join(data_folder, 'Data')

                    for file in os.listdir(data_folder_path):

                        file_path = os.path.join(data_folder_path, file)
                        print(file, ' removed')
                        os.remove(file_path)

                except Exception as e:

                    print(e)
                    QtGui.QMessageBox.information(MainWindow, "Oops!", "Could not delete the Data")


        self.start = QtGui.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(10, 10, 90, 25))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setObjectName(_fromUtf8("start"))

        self.start.clicked.connect(start_func)


        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(150, 10, 90, 25))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy)
        self.stop.setObjectName(_fromUtf8("stop"))

        self.stop.clicked.connect(stop_func)


        self.sendAction = QtGui.QPushButton(self.centralwidget)
        self.sendAction.setGeometry(QtCore.QRect(40, 160, 171, 91))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendAction.sizePolicy().hasHeightForWidth())
        self.sendAction.setSizePolicy(sizePolicy)
        self.sendAction.setObjectName(_fromUtf8("sendAction"))

        self.sendAction.clicked.connect(send_func)



        self.gitHub = QtGui.QPushButton(self.centralwidget)
        self.gitHub.setGeometry(QtCore.QRect(10, 90, 231, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gitHub.sizePolicy().hasHeightForWidth())
        self.gitHub.setSizePolicy(sizePolicy)
        self.gitHub.setObjectName(_fromUtf8("gitHub"))

        self.gitHub.clicked.connect(gitHub_func)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 250, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menubar)


        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)


        self.delLastDataAction = QtGui.QAction(MainWindow)
        self.delLastDataAction.setObjectName(_fromUtf8("delLastDataAction"))
        self.delLastDataAction.setStatusTip('Deletes the data from your last fishing session')

        self.delLastDataAction.triggered.connect(del_last_data)


        self.delDataAction = QtGui.QAction(MainWindow)
        self.delDataAction.setObjectName(_fromUtf8("delDataAction"))
        self.delDataAction.setStatusTip('Deletes all the data you gathered. Only do it if you really messed up when collecting data')

        self.delDataAction.triggered.connect(del_data)


        self.menuOptions.addAction(self.delLastDataAction)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.delDataAction)
        self.menubar.addAction(self.menuOptions.menuAction())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.start, self.stop)
        MainWindow.setTabOrder(self.stop, self.gitHub)
        MainWindow.setTabOrder(self.gitHub, self.sendAction)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Stardew Valley Fishing Bot", None))
        self.start.setText(_translate("MainWindow", "Start Collecting", None))
        self.stop.setText(_translate("MainWindow", "Stop Collecting", None))
        self.sendAction.setText(_translate("MainWindow", "Send", None))
        self.gitHub.setText(_translate("MainWindow", "Project GitHub", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.delLastDataAction.setText(_translate("MainWindow", "Delete Last Data", None))
        self.delDataAction.setText(_translate("MainWindow", "Delete All Data", None))




if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
