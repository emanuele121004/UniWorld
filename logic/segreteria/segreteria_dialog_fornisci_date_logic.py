import json
import os

from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QPushButton, QVBoxLayout, \
    QHBoxLayout
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile
from gui.segreteria.segreteria_dialog_fornisci_date import Ui_FornisciDate


class SegreteriaDialogFornisciDateLogic(QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_FornisciDate()
        self.ui.setupUi(self)
        self.ui.AggiornaButton.clicked.connect(self.aggiornaRichieste)
        self.data = None
        self.aggiornaRichieste()


    def aggiornaRichieste(self):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        rows = launchMethod(request_constructor_str({}, "GetRichiesteDateEsamiNonEvase"), server_coords['address'], server_coords['port'])
        rows = json.loads(rows)

        #print(rows)
        if rows["result"] == "false":
            QMessageBox.information(None, "Attenzione",
                                    f"Nessuna richiesta disponibile")
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

        print(data)

        del data[3]
        for d in data[1:]:
            layout.addWidget(QLabel(d))

        button_layout = QVBoxLayout()

        newButton_approve = QPushButton("Fornisci Date")
        newButton_approve.clicked.connect(lambda: self.Fornisci(data[0]))
        button_layout.addWidget(newButton_approve)

        newButton_decline = QPushButton("Rifiuta")
        newButton_decline.clicked.connect(lambda: self.rifiutaRichiesta(data[0]))
        button_layout.addWidget(newButton_decline)

        layout.addLayout(button_layout)

        # Set the layout of the widget
        self.ui.TableView.addLayout(layout)

    def Fornisci(self, ID:str):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        row = launchMethod(request_constructor_str({"ID":ID, "isAccettata":"1"}, "AggiornaRichiestaDate"), server_coords['address'], server_coords['port'])
        row = json.loads(row)

        QMessageBox.information(None, "Accept - Success","Richiesta accetta con successo")

        self.clearTableView()
        self.aggiornaRichieste()

    def rifiutaRichiesta(self, ID:str):
        ROOT_DIR = os.path.abspath(os.curdir)
        server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
        row = launchMethod(request_constructor_str({"ID":ID, "isAccettata":"0"}, "AggiornaRichiestaData"), server_coords['address'], server_coords['port'])
        row = json.loads(row)

        QMessageBox.information(None, "Decline - Success", "Richiesta rifiutata con successo")

        self.clearTableView()
        self.aggiornaRichieste()

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


