import json
import os
import re

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.students.students_dialog_prenotazioni_gui import Ui_Lista_Appelli



class StudentsDialogPrenotazioneLogic(QDialog):

    def __init__(self, user):
        super().__init__()
        self.dataToShow = "All"
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        self.user = user
        self.ui = Ui_Lista_Appelli()
        self.ui.setupUi(self)
        self.ui.CorsoLaureaLabel.setText(f"{self.user[6][0]} - {self.user[6][1]}")

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
                print("All")

                rows = json.loads(launchMethod(request_constructor_str(payload, "GetPrenotazioniAppelliByMatricola"),
                                               server_coords['address'], server_coords['port']))
            case "Evase":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetPrenotazioniAppelliByMatricolaEvase"),
                                 server_coords['address'], server_coords['port']))
            case "Accettate":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetPrenotazioniAppelliByMatricolaAccettate"),
                                 server_coords['address'], server_coords['port']))
            case "Rifiutate":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetPrenotazioniAppelliByMatricolaRifiutate"),
                                 server_coords['address'], server_coords['port']))
            case "Attesa":
                rows = json.loads(
                    launchMethod(request_constructor_str(payload, "GetPrenotazioniAppelliByMatricolaAttesa"),
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

    def createRow(self, data):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"{data[0]}/{data[4]}"))
        layout.addWidget(QLabel(data[1]))
        layout.addWidget(QLabel(data[2]))
        layout.addWidget(QLabel(data[3]))

        if data[5] == "?":
            label = QLabel("In attesa")
            label.setStyleSheet('color: GoldenRod')
            layout.addWidget(label)
        elif data[5] == "0":
            label = QLabel("Rifiutata")
            label.setStyleSheet('color: red')
            layout.addWidget(label)
        elif data[5] == "1":
            label = QLabel("Accetta")
            label.setStyleSheet('color: green')
            layout.addWidget(label)
        elif data[5] == "3":
            label = QLabel("Evasa")
            label.setStyleSheet('color: black')
            layout.addWidget(label)

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
    dialog = StudentsDialogPrenotazioneLogic()
    dialog.exec_()


if __name__ == "__main__":
    run()
