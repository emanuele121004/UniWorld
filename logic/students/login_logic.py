import json
import os
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import customHash, request_constructor_str, loadJSONFromFile
from gui.login_gui import Ui_Login


class LoginLogic(QMainWindow):

    show_students_home = pyqtSignal()
    show_office_home = pyqtSignal()
    user = []

    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.setWindowTitle("UniWorld - Login")
        self.ui.LoginButton.clicked.connect(self.checkLogin)

    def checkLogin(self):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        password = str(customHash(self.ui.PasswordField.text()))
        username = self.ui.EmailField.text()
        combobox = self.ui.ComboBoxSelect.currentText()
        result = None

        if combobox == "Students":
            toSend = {"Matricola": username, "Password": password}
            result = launchMethod(request_constructor_str(toSend, "StudentsLogin"), server_coords['address'], server_coords['port'])

        elif combobox == "Office":
            toSend = {"Email": username, "Password": password}
            result = launchMethod(request_constructor_str(toSend, "OfficeLogin"), server_coords['address'], server_coords['port'])

        result = result.replace("\n", "")
        result = result.replace("\r", "")
        if result == "false":
            QMessageBox.critical(None, "Login - Error",
                                 "Email, Password or User type incorrect.\nCheck your info and retry.")
        else:
            try:
                if combobox == "Students":
                    self.openStudentHomeWindow(result)
                if combobox == "Office":
                    self.openSegreteriaHomeWindow(result)
            except Exception as e:
                print(e)

    def openStudentHomeWindow(self, user):
        self.user = json.loads(user)
        self.show_students_home.emit()
        self.close()


    def openSegreteriaHomeWindow(self, user):
        self.user = json.loads(user)
        self.show_office_home.emit()
        self.close()


def run():
    app = QApplication(sys.argv)
    window = LoginLogic()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
