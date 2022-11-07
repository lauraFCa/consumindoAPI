from PyQt6.QtWidgets import ( QApplication, QWidget, QFormLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel )
from JanelaDadosPessoais import DadosPessoais


class OptionsWindow(QWidget):

    clearStyle = "font-size: small; color: rgba(0, 0, 0, .6)"
    titleStyle = "font-size: large; font-weight: bold"
    
    def __init__(self, tk):
        """Janela com opcoes de acao
        """
        super().__init__(parent=None)
        self.setMinimumSize(640, 360)
        self.token = tk
        self.setOpcoesLayout()


    def setOpcoesLayout(self):
        """Cria o layout desta janela (opções)
        """
        self.setWindowTitle("Ações")
        formLayout = QFormLayout()

        layoutVdados = QVBoxLayout() # layout vertical - informacoes Dados
        layoutVdados.addWidget(QLabel(f"<p><span style='{self.titleStyle}'> Obeter dados pessoais:</span><br>Dados como: Nome, imagem, localizalção da conta, país e idioma e Identificador</p>"))

        layoutVpublicacoes = QVBoxLayout() # layout vertical - informacoes Publicações
        layoutVpublicacoes.addWidget(QLabel(f"<p><span style='{self.titleStyle}'> Criar publicações:</span><br>Criar publicações no perfil do token contendo textos, imagens, hiperlinks, títulos, etc.</p>"))

        layoutH = QHBoxLayout() # layout horizontal - botoes

        dadosP = QPushButton("Obter dados pessoais")
        dadosP.clicked.connect(self.openDadosPessoais)
        layoutH.addWidget(dadosP)

        pub = QPushButton("Criar publicações")
        pub.clicked.connect(self.openPublicacoes)
        layoutH.addWidget(pub)

        voltar = QPushButton("Impimir token")
        voltar.setStyleSheet("color: #fff; background-color: #c5c5c5; border-radius: 3px; padding: 5px")
        voltar.clicked.connect(lambda:self.imprimirToken())

        formLayout.addRow(layoutVdados)
        formLayout.addRow(layoutVpublicacoes)
        formLayout.addRow(layoutH)
        formLayout.addRow(voltar)

        self.setLayout(formLayout)


    def openDadosPessoais(self):
        personal = DadosPessoais(self.token)
        personal.show()
        # self.hide()

    def openPublicacoes(self):
        pass

    def imprimirToken(self):
        print(self.token)
