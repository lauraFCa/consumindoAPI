import sys
from PyQt6.QtWidgets import ( QApplication, QWidget, QFormLayout, QPushButton, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel )
from JanelaOpcoes import OptionsWindow

class MainWindow(QWidget):

    clearStyle = "font-size: small; color: rgba(0, 0, 0, .6)"
    titleStyle = "font-size: large; font-weight: bold"
    msgErro = ''

    def __init__(self):
        """Janela principal
        """
        super().__init__(parent=None)
        self.setMinimumSize(640, 360)
        self.setPrincipalLayout()
        self.token = '' 
        self.mostrarMain = True

    def getToken(self): return self.token
    def getMostrarMain(self): return self.mostrarMain

    def setPrincipalLayout(self):
        """Cria o layout desta janela (principal)
        """
        self.setWindowTitle("Autenticação")
        formLayout = QFormLayout() # layout principal da janela

        layoutV = QVBoxLayout()  # layout vertical - organiza os horizontais
        layoutH = QHBoxLayout() # layout horizontal - botoes

        layoutV.addWidget(QLabel(f"<span style='{self.titleStyle}'>Informe o oauth token para autenticação na API</span>"))
        layoutV.addWidget(QLabel(f"Token: <span style='{self.clearStyle}'><br>Cole seu oauth token abaixo</span>"))
        self.tokenArea = QPlainTextEdit(self)
        layoutV.addWidget(self.tokenArea)

        layoutV.addWidget(QLabel(self.msgErro))

        buttonOk = QPushButton("Autenticar")
        buttonOk.clicked.connect(self.checkToken)

        buttonCancelar = QPushButton("Cancelar")
        buttonCancelar.clicked.connect(self.close)

        layoutH.addWidget(buttonOk)
        layoutH.addWidget(buttonCancelar)

        formLayout.addRow(layoutV)
        formLayout.addRow(layoutH)
        
        self.setLayout(formLayout)


    def checkToken(self):
        """Recupera o valor do token inserido
        """
        self.token = self.tokenArea.toPlainText()
        if(self.token == '' or len(self.token) < 100):
            self.msgErro = "<span style='color: red; font-weight: 700'>Preencha um token válido!</span>"
            print(self.msgErro)
            print(self.token)
            print(len(self.token))
        else:
            self.mostrarMain = False
            OptionsWindow(self.token).show()
            # self.hide()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(app.exec())


