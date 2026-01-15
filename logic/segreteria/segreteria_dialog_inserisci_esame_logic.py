import json
import os

from PyQt5.QtWidgets import QMessageBox, QDialog
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.segreteria.segreteria_dialog_inserisci_esame_gui import Ui_segreteria_dialog_inserisci_esame


class SegreteriaDialogInserisciEsameLogic(QDialog):

    def __init__(self):
        super().__init__()
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        self.ui = Ui_segreteria_dialog_inserisci_esame()
        self.ui.setupUi(self)
        result = launchMethod(request_constructor_str({}, "GetLauree"), server_coords['address'], server_coords['port'])
        result = json.loads(result)
        for item in result["result"]:
            self.ui.comboBoxLaurea.addItem(f"{item[0]} - {item[1]}")
            self.ui.comboBoxLaurea.setItemData(self.ui.comboBoxLaurea.count() - 1, item[0])
        self.ui.InsertEsameButton.clicked.connect(self.insertEsameIntoServer)

    def insertEsameIntoServer(self):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        selected_index = self.ui.comboBoxLaurea.currentIndex()
        item_data = self.ui.comboBoxLaurea.itemData(selected_index)
        toSend = {"CFU": str(self.ui.CFUSpinBox.text()), "NomeCorso": str(self.ui.NomeEsameField.text()), "IdCorso": str(self.ui.IDEsame.text()).upper(), "NomeProfessore": str(self.ui.NomeProfessoreField.text()), "Laurea":str(item_data)}
        result = launchMethod(request_constructor_str(toSend, "InsertCorso"), server_coords['address'], server_coords['port'])
        result = json.loads(result)

        if result["result"] != "True":
            QMessageBox.critical(None, "Insert - Error",
                                 f"L'esame inserito è già presente nel database\n{result['result'][0]} - {result['result'][1]} - {result['result'][2]} - {result['result'][3]} - {result['result'][4]}")
        else:
            QMessageBox.information(None, "Insert - Success",
                                 f"Esame Inserito correttamente")

def run():
    dialog = SegreteriaDialogInserisciEsameLogic()
    dialog.exec_()


if __name__ == "__main__":
    run()
