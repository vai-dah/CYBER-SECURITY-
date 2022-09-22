#!/usr/bin/python3
"""


"""

import os

from PyQt5 import QtCore, QtGui, QtWidgets
import lsb_steganography as stego
import mysql.connector


def convert_data(data, file_name):
    # Convert binary format to images
    # or files data(with given file_name)
    with open(file_name, 'wb') as file:
        file.write(data)


try:
    # establish connection
    connection = mysql.connector.connect(host="stegano.xyz",
                                         user="softpksx",
                                         password="Softpoint@#123",
                                         database="softpksx_python_data")
    cursor = connection.cursor()
    # getting data by id value
    query = """ SELECT * from python_table """

    id = 5
    cursor.execute(query)
    records = cursor.fetchall()
    for row in records:
        print("Image Id = ", row[0])
        image = row[2]
        # Pass path with filename where we want to save our file
        convert_data(image, "C:\sd\image" + str(row[0]) + ".png")
        # Pass path with filename where we want to save our file
        print("Successfully Retrieved Values from database")

except mysql.connector.Error as error:
    print(format(error))

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


class Ui_MainWindow(object):

    def fetchData(self):
        try:
            # establish connection
            connection = mysql.connector.connect(host="stegano.xyz",
                                                 user="softpksx",
                                                 password="Softpoint@#123",
                                                 database="softpksx_python_data")
            cursor = connection.cursor()
            # getting data by id value
            query = """ SELECT * from python_table """

            id = 5
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                print("Image Id = ", row[0])
                image = row[2]
                # Pass path with filename where we want to save our file
                convert_data(image, "C:\sd\image" + str(row[0]) + ".png")
                # Pass path with filename where we want to save our file
                print("Successfully Retrieved Values from database")

        except mysql.connector.Error as error:
            print(format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def insertBLOB(self, emp_id, photo):

        try:
            connection = mysql.connector.connect(host="stegano.xyz",
                                                 user="softpksx",
                                                 password="Softpoint@#123",
                                                 database="softpksx_python_data")

            cursor = connection.cursor()
            sql_insert_blob_query = """ INSERT INTO python_table
                              (photo_id, photo) VALUES (%s,%s)"""

            empPicture = self.convertToBinaryData(photo)

            # Convert data into tuple format
            insert_blob_tuple = (emp_id, empPicture)
            result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            connection.commit()
            print("Image and file inserted successfully as a BLOB into python_employee table", result)

        except mysql.connector.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def convertToBinaryData(self, filename):
        print(filename)
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    # Function to display message/error/information
    def displayMsg(self, title, msg, ico_type=None):
        MsgBox = QtWidgets.QMessageBox()
        MsgBox.setText(msg)
        MsgBox.setWindowTitle(title)
        if ico_type == 'err':
            ico = QtWidgets.QMessageBox.Critical
        else:
            ico = QtWidgets.QMessageBox.Information
        MsgBox.setIcon(ico)
        MsgBox.exec()

    # Function to choose input file
    def getFile(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', "Image files (*.jpg *.png *.bmp)")[0]
        if file_path != '':
            self.lineEdit.setText(file_path)

        # Function to choose input file

    def gettxtFile(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', "Image files (*.txt *.pdf)")[0]
        if file_path != '':
            self.file_txt.setText(file_path)

            filename = file_path

            # Open the file
            infile = open(filename,
                          'r')  # 'r' says we are opening the file to read, infile is the opened file object that we will read from

            # Store the data from the file in a variable
            data = infile.read()

            # Print the data in the file

            print(data)
            self.plainTextEdit.insertPlainText(data)

            # close the file
            infile.close()

    # Function to display save file dialog
    def saveFile(self):
        output_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save encoded file', '', "PNG File(*.png)")[0]
        return output_path

    # Function to encode data and save file
    def encode(self):
        input_path = self.lineEdit.text()
        text = self.plainTextEdit.toPlainText()
        password = self.lineEdit_2.text()

        if input_path == '':
            self.displayMsg('Error: No file chosen', 'You must select input image file!', 'err')

        elif text == '':
            self.displayMsg('Text is empty', 'Please enter some text to hide!')
        elif password == '':
            self.displayMsg('Error: No password given', 'Please enter a password!', 'err')
        else:
            output_path = self.saveFile()
            if output_path == '':
                self.displayMsg('Operation cancelled', 'Operation cancelled by user!')
            else:
                try:
                    loss = stego.encode(input_path, text, output_path, password, self.progressBar)
                except stego.FileError as fe:
                    self.displayMsg('File Error', str(fe), 'err')
                except stego.DataError as de:
                    self.displayMsg('Data Error', str(de), 'err')
                else:
                    self.displayMsg('Success', 'Encoded Successfully!\n\nImage Data Loss = {:.5f} %'.format(loss))
                    # self.displayMsg('Success', output_path)
                    self.progressBar.setValue(0)
                    self.insertBLOB(1, output_path)
                    self.fetchData()

    # Function to decode data
    def decode(self):
        input_path = self.lineEdit.text()
        password = self.lineEdit_3.text()

        if input_path == '':
            self.displayMsg('Error: No file chosen', 'You must select input image file!', 'err')

        elif password == '':
            self.displayMsg('Error: No password given', 'Please enter a password!', 'err')
        else:
            try:
                data = stego.decode(input_path, password, self.progressBar_2)
            except stego.FileError as fe:
                self.displayMsg('File Error', str(fe), 'err')
            except stego.FileError as fe1:
                self.displayMsg('File Error', str(fe1), 'err')
            except stego.PasswordError as pe:
                self.displayMsg('Password Error', str(pe), 'err')
                self.progressBar_2.setValue(0)
            else:
                self.displayMsg('Success', 'Decoded successfully!')
                self.plainTextEdit_2.document().setPlainText(data)
                MainWindow.show()
                self.progressBar_2.setValue(0)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 575)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet('QLabel,QPushButton,QLineEdit,QPlainTextEdit{font-size: 11pt;}'
                                 'QPushButton { color: white; background-color: #fc034e; font-weight: bold}')

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.label_txt = QtWidgets.QLabel(self.centralwidget)
        self.label_txt.setObjectName("label_txt")
        self.verticalLayout.addWidget(self.label_txt)

        self.file_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.file_txt.setObjectName("file_txt")
        self.verticalLayout.addWidget(self.file_txt)

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setAutoFillBackground(False)
        self.pushButton1.setAutoDefault(True)
        self.pushButton1.setObjectName("pushButton1")
        self.verticalLayout.addWidget(self.pushButton1)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_6.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_4.addWidget(self.checkBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem10)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setEnabled(True)
        self.progressBar_2.setMaximum(100)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setTextVisible(True)
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout_7.addWidget(self.progressBar_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem12)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout_3.addWidget(self.plainTextEdit_2)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Slots
        self.pushButton.clicked.connect(self.getFile)
        self.pushButton1.clicked.connect(self.gettxtFile)
        self.pushButton_2.clicked.connect(self.encode)
        self.pushButton_3.clicked.connect(self.decode)
        self.checkBox.stateChanged.connect(lambda: self.lineEdit_2.setEchoMode(
            QtWidgets.QLineEdit.Normal) if self.checkBox.isChecked() else self.lineEdit_2.setEchoMode(
            QtWidgets.QLineEdit.Password))
        self.checkBox_2.stateChanged.connect(lambda: self.lineEdit_3.setEchoMode(
            QtWidgets.QLineEdit.Normal) if self.checkBox_2.isChecked() else self.lineEdit_3.setEchoMode(
            QtWidgets.QLineEdit.Password))

        # Menu action
        self.actionAbout.triggered.connect(lambda: self.displayMsg('About',
                                                                   'Created by: Vaidehi Dayaram Dahare\n\nVellore Institude of Technology, Vellore'))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Steganography Software"))
        self.label_4.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-weight:600;\"></span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Input Image File:"))
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.pushButton1.setText(_translate("MainWindow", "Choose File"))

        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#a30000;\">ENCODE</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#280154;\">DECODE</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-weight:600;\"></span></p></body></html>"))

        self.label_txt.setText(_translate("MainWindow", "Input Text File:"))
        self.label_7.setText(_translate("MainWindow", "OR Enter text to hide:"))
        self.label_8.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-weight:600;\"></span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "Enter Password:"))
        self.checkBox.setText(_translate("MainWindow", "Show Password"))
        self.label_11.setText(_translate("MainWindow", "Progress:"))
        self.pushButton_2.setText(_translate("MainWindow", "Encode and Save"))
        self.label_6.setText(_translate("MainWindow",
                                        "<html><head/><body><p><span style=\" font-weight:600;\"></span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Enter Password:"))
        self.checkBox_2.setText(_translate("MainWindow", "Show Password"))
        self.pushButton_3.setText(_translate("MainWindow", "Decode"))
        self.label_13.setText(_translate("MainWindow", "Progress:"))
        self.label_12.setText(_translate("MainWindow", "Decoded Data:"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

