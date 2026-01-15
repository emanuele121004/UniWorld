import json
import os
import re

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.students.students_dialog_invio_richiesta_date_esami_gui import Ui_Invio_Richiesta_Date_Esami
from logic.students.students_dialog_seleziona_appello_logic import StudentsDialogRichiestaPrenotazioneLogic


class StudentsDialogRichiestaDateLogic(QDialog):

    def __init__(self, user):
        super().__init__()
        self.dataToShow = "All"
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        self.user = user
        self.ui = Ui_Invio_Richiesta_Date_Esami()
        self.ui.setupUi(self)
        self.ui.CorsoLaureaLabel.setText(f"{self.user[6][0]} - {self.user[6][1]}")
        corsi = json.loads(
            launchMethod(request_constructor_str(None, "GetCorsi"), server_coords['address'], server_coords['port']))
        corsi = corsi['result']
        for c in corsi:
            if str(c[4]) == str(self.user[6][0]):
                newstr = f"[{c[0]}] {c[2]} - {c[1]} CFU"
                self.ui.comboBox.addItem(newstr)
        self.ui.InviaRichiestaButton.clicked.connect(self.inviaRichiesta)
        self.ui.AggiornaStoricoButton.clicked.connect(self.aggiornaStorico)

        self.ui.TutteRadio.toggled.connect(lambda checked: self.onRadioToggled("All", checked))
        self.ui.EvaseRadio.toggled.connect(lambda checked: self.onRadioToggled("Evase", checked))
        self.ui.AccettateRadio.toggled.connect(lambda checked: self.onRadioToggled("Accettate", checked))
        self.ui.RifiutateRadio.toggled.connect(lambda checked: self.onRadioToggled("Rifiutate", checked))
        self.ui.AttesaRadio.toggled.connect(lambda checked: self.onRadioToggled("Attesa", checked))


        self.data = None
        self.aggiornaStorico()

    def onRadioToggled(self, update: str, checked: bool):
        if checked:
            self.updateDataToShow(update)

    def updateDataToShow(self, update: str):
        self.dataToShow = str(update)
        self.aggiornaStorico()

    def aggiornaStorico(self):
        payload = {"Matricola": self.user[0]}
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        rows = None

        match self.dataToShow:
            case "All":
                rows = json.loads(launchMethod(request_constructor_str(payload, "GetRichiesteDateEsamiByMatricola"),
                                               server_coords['address'], server_coords['port']))
            case "Evase":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetRichiesteDateEsamiByMatricolaEvase"),
                                 server_coords['address'], server_coords['port']))
            case "Accettate":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetRichiesteDateEsamiByMatricolaAccettate"),
                                 server_coords['address'], server_coords['port']))
            case "Rifiutate":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetRichiesteDateEsamiByMatricolaRifiutate"),
                                 server_coords['address'], server_coords['port']))
            case "Attesa":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetRichiesteDateEsamiByMatricolaAttesa"),
                                 server_coords['address'], server_coords['port']))

        print(rows)
        if rows["result"] == "false":
            QMessageBox.information(None, "Attenzione",
                                    f"Nessuna richiesta disponibile")
            self.clearTableView()
            self.data = None
        else:
            if self.data == None:
                for r in rows["result"]:
                    self.createRow(r)
                self.data = rows
            elif self.data != rows:
                self.data = rows
                self.clearTableView()
                for r in rows["result"]:
                    self.createRow(r)

    def inviaRichiesta(self):
        selected = self.ui.comboBox.currentText()
        pattern = r'\[(.*?)\]'
        selected = re.search(pattern, selected)
        selected = selected.group(1)
        payload = {"EsameRichiesto": selected, "MatricolaRichiedente": self.user[0]}
        print(f"Payload: {payload}")
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        result = launchMethod(request_constructor_str(payload, "PutDataRichiestaDate"), server_coords['address'],
                              server_coords['port'])
        result = json.loads(result)
        if result['result'] == "OK":
            QMessageBox.information(None, "Accept - Success", "Richiesta Inviata con successo")
        self.clearTableView()
        self.aggiornaStorico()

    def createRow(self, data):
        layout = QHBoxLayout()

        layout.addWidget(QLabel(data[0]))
        layout.addWidget(QLabel(data[1]))

        newButton_mostradate = QPushButton("Mostra date")
        newButton_mostradate.clicked.connect(lambda: self.showDialogDates(data[0], data[3]))

        if data[2] == "?":
            label = QLabel("In attesa")
            label.setStyleSheet('color: GoldenRod')
            layout.addWidget(label)
            newButton_mostradate.setEnabled(False)
        elif data[2] == "0":
            label = QLabel("Rifiutata")
            label.setStyleSheet('color: red')
            layout.addWidget(label)
            newButton_mostradate.setEnabled(False)
        elif data[2] == "1":
            label = QLabel("Accetta")
            label.setStyleSheet('color: green')
            layout.addWidget(label)
            newButton_mostradate.setEnabled(True)
        elif data[2] == "3":
            label = QLabel("Evasa")
            label.setStyleSheet('color: black')
            layout.addWidget(label)
            newButton_mostradate.setEnabled(False)

        layout.addWidget(newButton_mostradate)

        # Set the layout of the widget
        self.ui.TableView.addLayout(layout)

    def showDialogDates(self, id, data):
        data = data.replace("'", '"')
        data = json.loads(data)
        if len(data['dates']) == 0:
            QMessageBox.information(None, "Accept - Success", "Non sono state aconra definite date per questo corso")
            return

        data["id_request"] = id
        dialog = StudentsDialogRichiestaPrenotazioneLogic(self.user, data)
        dialog.exec_()
        self.clearTableView()
        self.aggiornaStorico()

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
    dialog = StudentsDialogRichiestaDateLogic()
    dialog.exec_()


if __name__ == "__main__":
    run()
