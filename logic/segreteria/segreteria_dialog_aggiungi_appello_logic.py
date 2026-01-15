import json
import os
import re

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QDialog

# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.segreteria.segreteria_dialog_inserisci_appello_gui import Ui_segreteria_dialog_inserisci_appello


class SegreteriaDialogAggiungiappelloLogic(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_segreteria_dialog_inserisci_appello()
        self.ui.setupUi(self)
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        corsi = json.loads(
            launchMethod(request_constructor_str(None, "GetCorsi"), server_coords['address'], server_coords['port']))
        corsi = corsi['result']
        for c in corsi:
            newstr = f"[{c[0]}] {c[2]} - {c[1]} CFU"
            self.ui.comboBoxCorsi.addItem(newstr)

        self.ui.InsertAppelloButton.clicked.connect(self.inserisciAppello)
        self.ui.dateTimeEdit.setCalendarPopup(True)

    def inserisciAppello(self):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))

        selected = self.ui.comboBoxCorsi.currentText()
        pattern = r'\[(.*?)\]'
        selected = re.search(pattern, selected)
        corso = selected.group(1)
        Luogo = self.ui.Luogo.toPlainText()
        time = self.ui.dateTimeEdit.text()
        time = time.replace("/", "-")
        time = time.replace("\\", ".")
        payload = {
            "corso": corso,
            "luogo": Luogo,
            "time": time + ":00"
        }

        res = launchMethod(request_constructor_str(payload, 'inserisciAppello'), server_coords['address'], server_coords['port'])
        res = json.loads(res)
        if res["result"] == 'OK':
            QMessageBox.information(None, "Success", "Appello inserito con successo")
        print(res)


def run():
    dialog = Ui_segreteria_dialog_inserisci_appello()
    dialog.exec_()


if __name__ == "__main__":
    run()
