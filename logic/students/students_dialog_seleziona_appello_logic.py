import json
import os
import re

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.students.students_dialog_select_appello import Ui_student_dialog_select_appello


class StudentsDialogRichiestaPrenotazioneLogic(QDialog):

    def __init__(self,user,data):
        super().__init__()
        self.data = data
        self.user = user
        self.ui = Ui_student_dialog_select_appello()
        self.ui.setupUi(self)
        self.ui.RichiestaLabel.setText(f"{data['id_request']}")
        self.ui.CorsoLabel.setText(f"{data['dates'][0][2]}")
        self.aggiornaStorico()

    def aggiornaStorico(self):
        rows = self.data
        for r in rows["dates"]:
            self.createRow(r)

    def inviaRichiesta(self,data):
        payload = {"ID_Richiesta":self.data['id_request'], "ID_Appello": data[0], "MatricolaRichiedente": self.user[0]}
        print(f"Payload: {payload}")
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))

        result = launchMethod(request_constructor_str(payload, "PutDataRichiestaPrenotazione"), server_coords['address'], server_coords['port'])
        result = json.loads(result)
        if result['result'] == "OK":
            QMessageBox.information(None, "Accept - Success", "Richiesta di prenotazione inviata con successo")
        self.close()

    def createRow(self, data):
        layout = QHBoxLayout()


        layout.addWidget(QLabel(data[0]))
        layout.addWidget(QLabel(data[1]))

        newButton_prenotazione = QPushButton("Prenota Appello")
        newButton_prenotazione.clicked.connect(lambda: self.inviaRichiesta(data[0]))

        layout.addWidget(newButton_prenotazione)

        # Set the layout of the widget
        self.ui.TableView.addLayout(layout)

    def clearTableView(self):
        # Remove all layouts from TableView
        while self.ui.TableView.count():
            item = self.ui.TableView.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    layout = item.layout()
                    if layout:
                        # Recursively clear layout's items
                        self.clearLayout(layout)

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clearLayout(item.layout())


def run():
    dialog = StudentsDialogRichiestaPrenotazioneLogic()
    dialog.exec_()


if __name__ == "__main__":
    run()
