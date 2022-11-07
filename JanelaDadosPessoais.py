from PyQt6.QtWidgets import ( QApplication, QWidget, QFormLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel )
from server import ServerMethods
import json


class DadosPessoais(QWidget):

    url = "https://api.linkedin.com/v2"
    infosP = ''

    def __init__(self, tk):
        """Janela com opcoes de acao
        """
        super().__init__(parent=None)
        self.setMinimumSize(640, 360)
        self.setDadosLayout()
        self.token = tk


    def setDadosLayout(self):
        """Cria o layout desta janela (dados pessoais)
        """
        self.setWindowTitle("Dados pessoais")
        formLayout = QFormLayout()

        layoutVdados = QVBoxLayout() # layout vertical - informacoes Dados
        self.label_2 = QLabel("", self)
        layoutVdados.addWidget(self.label_2)

        layoutVpublicacoes = QVBoxLayout() # layout vertical - informacoes Publicações

        layoutH = QHBoxLayout() # layout horizontal - botoes

        dadosP = QPushButton("Obter dados")
        dadosP.clicked.connect(self.getDadosPessoais)
        layoutH.addWidget(dadosP)

        layoutVpublicacoes.addWidget(QLabel("<b>Dados adicionais:</b>"))

        dadosAdd = QPushButton("Dados adicionais")
        dadosAdd.clicked.connect(self.setarValoresDetalhes)
        layoutH.addWidget(dadosAdd)

        formLayout.addRow(layoutVdados)
        formLayout.addRow(layoutVpublicacoes)
        formLayout.addRow(layoutH)

        self.setLayout(formLayout)


    def getDadosPessoais(self):
        self.sm = ServerMethods(self.url, self.token)

        self.infosP = self.sm.getPersonBasicInfo()
        self.infosP = json.dumps(self.infosP)
        self.infosP = json.loads(self.infosP)

        self.Id = self.infosP["id"]
        self.label_2.setText(f"Id: {self.Id}")
        self.localizedFirstName = self.infosP["localizedFirstName"]
        self.localizedLastName = self.infosP["localizedLastName"]
        self.profilePicture = self.infosP["profilePicture"]
        self.displayImage = self.profilePicture["displayImage"]

        self.firstName = self.infosP["firstName"]
        self.localizedInFirstName = self.firstName["localized"]
        self.pt_BRinFirstName = self.localizedInFirstName["pt_BR"]
        self.preferredLocaleinFirstName = self.firstName["preferredLocale"]
        self.countryInFirstName = self.preferredLocaleinFirstName["country"]
        self.languageInFirstName = self.preferredLocaleinFirstName["language"]

        self.lastName = self.infosP["lastName"]
        self.localizedInLastName = self.lastName["localized"]
        self.pt_BRinLastName = self.localizedInLastName["pt_BR"]
        self.preferredLocaleinLastName = self.lastName["preferredLocale"]
        self.countryInLastName = self.preferredLocaleinLastName["country"]
        self.languageInLastName = self.preferredLocaleinLastName["language"]


    def setarValoresBasicos(self):
        print(self.infosP)
        pass

    def setarValoresDetalhes(self):
        pass
