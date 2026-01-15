from PyQt5.QtWidgets import QMainWindow
# from pyqt5_plugins.examplebutton import QtWidgets
from common.communication import find_rows

from common.communication import formato_data
from gui.segreteria.segreteria_home_gui import Ui_Segreteria_Home
from logic.segreteria.segreteria_dialog_inserisci_laurea_logic import SegreteriaDialogInserisciLaureaLogic
from logic.segreteria.segreteria_dialog_inserisci_esame_logic import SegreteriaDialogInserisciEsameLogic
from logic.segreteria.segreteria_dialog_inoltra_prenotazione_logic import SegreteriaDialogInoltraPrenotazioneLogic
from logic.segreteria.segreteria_dialog_fornisci_date_logic import SegreteriaDialogFornisciDateLogic
from logic.segreteria.segreteria_dialog_aggiungi_appello_logic import SegreteriaDialogAggiungiappelloLogic


class SegreteriaHomeLogic(QMainWindow):
    user = None

    def __init__(self, user):
        self.user = user
        super().__init__()
        self.ui = Ui_Segreteria_Home()
        self.ui.setupUi(self)
        self.setWindowTitle("UniWorld - Segreteria")
        self.ui.InserimentoLaureaButton.clicked.connect(self.showDialogInserimentoLaurea)
        self.ui.InserimentoEsamiButton.clicked.connect(self.showDialogInserimentoEsame)
        self.ui.DateDiposnibiliEsami.clicked.connect(self.showDialogFornisciDate)
        self.ui.InoltraRichiestaButton.clicked.connect(self.showDialogInoltraPrenotazione)
        self.ui.AggiungiAppello.clicked.connect(self.showDialogAggiungiAppello)

    def showWindow(self, user):
        self.show()
        self.user = user
        self.ui.MtrLabel.setText(user[0])
        self.ui.NameLastnameLabel.setText(f"{user[1]}, {user[2]}")
        self.ui.DateLabel.setText(f"{formato_data()}")

    def showDialogInserimentoLaurea(self):
        dialog = SegreteriaDialogInserisciLaureaLogic()
        dialog.exec_()

    def showDialogInserimentoEsame(self):
        dialog = SegreteriaDialogInserisciEsameLogic()
        dialog.exec_()

    def showDialogInoltraPrenotazione(self):
        dialog = SegreteriaDialogInoltraPrenotazioneLogic()
        dialog.exec_()

    def showDialogFornisciDate(self):
        dialog = SegreteriaDialogFornisciDateLogic()
        dialog.exec_()

    def showDialogAggiungiAppello(self):
        dialog = SegreteriaDialogAggiungiappelloLogic()
        dialog.exec_()


def run(user):
    window = SegreteriaHomeLogic(user)
    window.show()


if __name__ == "__main__":
    run('["0124002584", "Vittorio", "Picone", "vittorio.picone001@studenti.uniparthenope.it", "1914752590"]')
