import requests, os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from ScrollLabel import ScrollLabel
from PyQt6.QtWidgets import (QComboBox, QFormLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPlainTextEdit, QPushButton,
                             QRadioButton, QVBoxLayout)


class Layouts:

    clearStyle = "font-size: small; color: rgba(0, 0, 0, .6)"
    titleStyle = "font-size: large; font-weight: bold"

    def setSplashJanela(self, thisWindow, iniciar):
        """Layout da primeira janela do sistema

        Args:
            thisWindow (PyQt6 Window): Splash Janela
            iniciar (function): Method to call next window
        """
        thisWindow.setWindowTitle("Autenticação")
        formLayout = QFormLayout()  # layout principal da janela
        
        imgLbl = QLabel()
        pxImg = QPixmap(os.path.join("imgs","integracaoSft.png"))
        imgLbl.setPixmap(pxImg.scaled(490, 490, Qt.AspectRatioMode.KeepAspectRatio))
        imgLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btnIniciar = QPushButton("Iniciar")
        btnIniciar.clicked.connect(iniciar)
        
        formLayout.addRow(QLabel("<h2>Trabalho desenvolvido para disciplina de Integração de Softesre - UniAcademia</h2>"))
        formLayout.addRow(imgLbl)
        formLayout.addRow(btnIniciar)
        thisWindow.setLayout(formLayout)

    # region Janela Principal
    def setPrincipalLayout(self, thisWindow, checkToken):
        """Layout da janela principal

        Args:
            thisWindow (PyQt6 Window): Splash Janela
            checkToken (function): Method to validate if inputed token is valid
        """
        thisWindow.setWindowTitle("Autenticação")
        formLayout = QFormLayout()  # layout principal da janela

        layoutV = QVBoxLayout()  # layout vertical - organiza os horizontais
        layoutH = QHBoxLayout()  # layout horizontal - botoes

        layoutV.addWidget(QLabel(
            f"<span style='{self.titleStyle}'>Informe o oauth token para autenticação na API</span>"))
        layoutV.addWidget(QLabel(
            f"Token: <span style='{self.clearStyle}'><br>Cole seu oauth token abaixo</span>"))
        self.msgErroLabel = QLabel("")
        self.tokenArea = QPlainTextEdit(thisWindow)

        layoutV.addWidget(self.tokenArea)
        layoutV.addWidget(self.msgErroLabel)

        buttonOk = QPushButton("Autenticar")
        buttonOk.clicked.connect(checkToken)

        buttonCancelar = QPushButton("Cancelar")
        buttonCancelar.clicked.connect(thisWindow.close)

        layoutH.addWidget(buttonOk)
        layoutH.addWidget(buttonCancelar)

        formLayout.addRow(layoutV)
        formLayout.addRow(layoutH)

        thisWindow.setLayout(formLayout)

    def returnToken(self):
        return self.tokenArea.toPlainText()

    def setMsgErro(self, erro):
        self.msgErroLabel.setText(erro)

    # endregion

    # region Janela de Opcoes
    def setOpcoesLayout(self, thisWindow, openDadosPessoais, openPublicacoes, token, voltar):
        """Layout da Janela com Opcoes

        Args:
            thisWindow (PyQt6 Window): Janela de opcoes
            openDadosPessoais (function): Metodo para abrir a janela de GET Dados
            openPublicacoes (function): Metodo para abrir a janela de POST publicacoes
            token (string): Token inserido pelo usuario na tela anterior
            voltar (function): Funcao para retornar a pagina anterior
        """
        self.tk = token
        thisWindow.setWindowTitle("Ações")
        formLayout = QFormLayout()

        layoutVdados = QVBoxLayout()  # layout vertical - informacoes Dados
        layoutVdados.addWidget(QLabel(
            f"<p><span style='{self.titleStyle}'> Obeter dados pessoais:</span><br>Dados como: Nome, imagem, localizalção da conta, país e idioma e Identificador</p>"))

        layoutVpublicacoes = QVBoxLayout()  # layout vertical - informacoes Publicações
        layoutVpublicacoes.addWidget(QLabel(
            f"<p><span style='{self.titleStyle}'> Criar publicações:</span><br>Criar publicações no perfil do token contendo textos, imagens, hiperlinks, títulos, etc.</p>"))

        layoutH = QHBoxLayout()  # layout horizontal - botoes

        dadosP = QPushButton("Obter dados pessoais")
        dadosP.clicked.connect(openDadosPessoais)
        layoutH.addWidget(dadosP)

        pub = QPushButton("Criar publicações")
        pub.clicked.connect(openPublicacoes)
        layoutH.addWidget(pub)

        showTkBtn = QPushButton("Impimir token")
        showTkBtn.setStyleSheet(
            "color: #fff; background-color: #c5c5c5; border-radius: 3px; padding: 5px")
        showTkBtn.clicked.connect(self.imprimirToken)

        btnVoltar = QPushButton("Voltar")
        btnVoltar.clicked.connect(voltar)

        btns = QHBoxLayout()
        btns.addWidget(showTkBtn)
        btns.addWidget(btnVoltar)

        self.tkLabel = QLabel("")
        self.tkLabel.setWordWrap(True)

        formLayout.addRow(layoutVdados)
        formLayout.addRow(layoutVpublicacoes)
        formLayout.addRow(layoutH)
        formLayout.addRow(btns)
        formLayout.addRow(self.tkLabel)

        thisWindow.setLayout(formLayout)

    def imprimirToken(self):
        self.tkLabel.setText(self.tk)

    # endregion

    # region Janela dos Dados Pessoais
    def setDadosLayout(self, thisWindow, getDadosPessoais, getMaisDados, inicializarCampos1, inicializarCampos2, mostrarJson, voltar):
        """Criar layout da janela de Obtencao de Dados 

        Args:
            thisWindow (PyQt6 Window): Janela de Dados
            getDadosPessoais (function): GET dados do usuario
            getMaisDados (function): GET dados extras do usuario
            inicializarCampos1 (function): Inicializa os campos para os dados pessoais
            inicializarCampos2 (function): Inicializa os campos mais dados pessoais
            mostrarJson (function): Printa o json recebido na tela
            voltar (function): Funcao para voltar a tela anterior
        """
        thisWindow.setWindowTitle("Dados pessoais")
        formLayout = QFormLayout()

        layoutHbtns = QHBoxLayout()  # layout horizontal - botoes

        dadosP = QPushButton("Obter dados")
        dadosP.clicked.connect(getDadosPessoais)
        layoutHbtns.addWidget(dadosP)

        dadosAdd = QPushButton("Dados adicionais")
        dadosAdd.clicked.connect(getMaisDados)
        layoutHbtns.addWidget(dadosAdd)

        layoutHdados = QHBoxLayout()

        self.labelsDoResultado1 = inicializarCampos1
        layoutVdados = QVBoxLayout()  # layout vertical - informacoes Dados
        for i in range(len(self.labelsDoResultado1)):
            layoutVdados.addWidget(self.labelsDoResultado1[i])

        layoutHdados.addItem(layoutVdados)

        self.labelsDoResultado2 = inicializarCampos2
        layoutVmaisDados = QVBoxLayout()  # layout vertical - informacoes Mais Dados
        for i in range(len(self.labelsDoResultado2)):
            layoutVmaisDados.addWidget(self.labelsDoResultado2[i])

        layoutHdados.addItem(layoutVmaisDados)

        jsonCom = QVBoxLayout()

        btnJson = QPushButton("Imprimir Json completo")
        btnJson.clicked.connect(mostrarJson)

        self.jsonComp1 = ScrollLabel()

        jsonCom.addWidget(btnJson)
        jsonCom.addWidget(self.jsonComp1)

        btnVoltar = QPushButton("Voltar")
        btnVoltar.clicked.connect(voltar)

        formLayout.addRow(layoutHbtns)
        formLayout.addRow(layoutHdados)
        formLayout.addRow(jsonCom)
        formLayout.addWidget(btnVoltar)

        thisWindow.setLayout(formLayout)

    def setarValores1NaTela(self, infosP):
        """Seta os valores obtidos do request de dados na tela

        Args:
            infosP (json): Resultado do primeiro request
        """
        self.labelsDoResultado1[0].setText(f"<h3>Dados</h3>")

        self.Id = infosP["id"]
        self.labelsDoResultado1[1].setText(f"<b>Id</b>: {self.Id}")

        self.localizedFirstName = infosP["localizedFirstName"]
        self.labelsDoResultado1[2].setText(
            f"<b>Nome</b>: {self.localizedFirstName}")

        self.localizedLastName = infosP["localizedLastName"]
        self.labelsDoResultado1[3].setText(
            f"<b>Sobrenome</b>: {self.localizedLastName}")

        self.profilePicture = infosP["profilePicture"]

        self.displayImage = self.profilePicture["displayImage"]
        self.labelsDoResultado1[4].setText(
            f"<b>Imagem de Perfil</b>: {self.displayImage}")

        self.firstName = infosP["firstName"]
        self.localizedInFirstName = self.firstName["localized"]
        self.pt_BRinFirstName = self.localizedInFirstName["pt_BR"]
        self.preferredLocaleinFirstName = self.firstName["preferredLocale"]

        self.labelsDoResultado1[5].setText(f"<h3>Localidade</h3>")

        self.countryInFirstName = self.preferredLocaleinFirstName["country"]
        self.labelsDoResultado1[6].setText(
            f"<b>País</b>: {self.countryInFirstName}")

        self.languageInFirstName = self.preferredLocaleinFirstName["language"]
        self.labelsDoResultado1[7].setText(
            f"<b>Idoma</b>: {self.languageInFirstName}")

        self.lastName = infosP["lastName"]
        self.localizedInLastName = self.lastName["localized"]
        self.pt_BRinLastName = self.localizedInLastName["pt_BR"]
        self.preferredLocaleinLastName = self.lastName["preferredLocale"]
        self.countryInLastName = self.preferredLocaleinLastName["country"]
        self.languageInLastName = self.preferredLocaleinLastName["language"]

    def getAndSetImageFromURL(self, imgLabel, imgPixMap, imageURL):
        """Adiciona a imagem de perfil recebida no request a tela

        Args:
            imgLabel (QLabel): Elemento onde a imagem ira entrar
            imgPixMap (QPixmap): Elemento de Imagem
            imageURL (string): URL da imagem de perfil, retornada no request
        """
        request = requests.get(imageURL)
        imgPixMap.loadFromData(request.content)
        imgLabel.setPixmap(imgPixMap)

    def setarValores2NaTela(self, maisInfos):
        """Seta os valores obtidos do request de dados extras na tela

        Args:
            infosP (json): Resultado do primeiro request
        """
        profPic = maisInfos["profilePicture"]
        dispImg = profPic["displayImage~"]
        self.elements = dispImg["elements"]

        authMeth = self.elements[0]["authorizationMethod"]
        self.labelsDoResultado2[1].setText(f"<b>Método</b>: {authMeth}")

        elements0 = self.elements[0]
        media = elements0["data"]["com.linkedin.digitalmedia.mediaartifact.StillImage"]

        mediaType = media["mediaType"]
        self.labelsDoResultado2[2].setText(
            f"<b>Tipo da Midia</b>: {mediaType}")

        tamanhos = media["displaySize"]
        self.labelsDoResultado2[3].setText(f"<h3>Tamanhos da Imagem</h3>")

        largura = tamanhos["width"]
        self.labelsDoResultado2[4].setText(f"<b>Largura</b>: {largura}")

        altura = tamanhos["height"]
        self.labelsDoResultado2[5].setText(f"<b>Altura</b>: {altura}")

        unidade = tamanhos["uom"]
        self.labelsDoResultado2[6].setText(f"<b>Unidade</b>: {unidade}")

        identifier = elements0["identifiers"][0]

        self.imgUrl = identifier["identifier"]
        self.labelsDoResultado2[7].setText(
            f"<b>Link da Imagem</b>: {self.imgUrl}")
        self.getAndSetImageFromURL(
            self.labelsDoResultado2[0], QPixmap(""), self.imgUrl)

        identifierType = identifier["identifierType"]
        self.labelsDoResultado2[8].setText(
            f"<b>Tipo de Link</b>: {identifierType}")

    def setarJsonNaTela(self, jsonC):
        self.jsonComp1.setText(jsonC)

    # endregion

    #region Janela de Publicacoes
    def setarPubLayout(self, thisWindow, getDataAndPost, voltar):
        """Layout da janela de Publicacoes

        Args:
            thisWindow (PyQt6 Window): Janela de criar Publicacoes
            getDataAndPost (function): Metodo para pegar os valores da tela e fazer o request
            voltar (function): Metodo para voltar a tela anterior
        """
        self.theW = thisWindow
        self.selectedVisibility, self.postTye = "PUBLIC", ""
        thisWindow.setWindowTitle("Criar nova Publicação")
        self.formLayout = QFormLayout()

        self.tipoPubLb = QLabel("Selecione o tipo de publicação:")

        # subregion Radio Buttons
        radioBtnLayout = QHBoxLayout()
        self.radio1 = QRadioButton("Simples", thisWindow)
        self.radio1.toggled.connect(self.loadSimpleFields)
        radioBtnLayout.addWidget(self.radio1)

        self.radio2 = QRadioButton("Com imagem", thisWindow)
        self.radio2.toggled.connect(self.loadImagensFields)
        radioBtnLayout.addWidget(self.radio2)

        self.radio3 = QRadioButton("Com Link (artigo)", thisWindow)
        self.radio3.toggled.connect(self.loadArtigoFields)
        radioBtnLayout.addWidget(self.radio3)
        # endsubregion

        comboBxPrivacidade = QComboBox()
        comboBxPrivacidade.addItems(['PUBLIC', 'CONNECTIONS'])

        self.labelConteudo = QLabel("Texto da publicação:")
        self.txtPub = QPlainTextEdit()

        # subregion Declaring extra fields
        self.simpleFields = QHBoxLayout()
        self.articleFields = QHBoxLayout()
        self.imagemFields = QHBoxLayout()
        self.linkTitle = QHBoxLayout()
        self.linkTxt = QHBoxLayout()
        self.linkUrl = QHBoxLayout()
        self.lblUrl = QLabel("URL do Link: ")
        self.linkUrlIn = QLineEdit()
        self.imgPath = QLineEdit()
        self.tituloLink = QLineEdit()
        self.imgAlt = QHBoxLayout()
        self.txtImg = QHBoxLayout()
        self.imgImg = QHBoxLayout()
        self.imgPath = QLineEdit()
        self.imgLbl = QLabel()
        self.aguardeLbl = QLabel()
        self.mediaTxt = QLineEdit()
        self.imgAlttxt = QLineEdit()
        self.aguardeLbl.setOpenExternalLinks(True)
        # endsubregion

        self.newLayout = QFormLayout()

        # subregion Buttons
        btnLayouts = QHBoxLayout()
        self.btnPostar = QPushButton("Publicar")
        self.btnPostar.clicked.connect(getDataAndPost)

        btnVoltar = QPushButton("Voltar")
        btnVoltar.clicked.connect(voltar)

        btnLayouts.addWidget(self.btnPostar)
        btnLayouts.addWidget(btnVoltar)
        # endsubregion

        vert = QVBoxLayout()
        vert.addWidget(QLabel(
            "<span style='font-size: small'>A seleção é aceita apenas uma vez. Para mudar o tipo de post é necessário voltar a tela anterior</span>"))
        self.formLayout.addRow(self.tipoPubLb)
        self.formLayout.addRow(radioBtnLayout)
        self.formLayout.addRow(vert)
        self.formLayout.addRow(
            "Visibilidade da Publicação: ", comboBxPrivacidade)
        self.formLayout.addRow(QLabel(
            "<span style='font-size: small'>Selecionando a opção 'Connections' é necessário estar na rede do usuário para visualizar o post"))
        self.formLayout.addRow(self.labelConteudo)
        self.formLayout.addRow(self.txtPub)
        self.formLayout.addRow(self.newLayout)

        self.formLayout.addRow(btnLayouts)

        thisWindow.setLayout(self.formLayout)


    def selecionado(self, index):
        """Identifica a visibilidade do post selecionado

        Args:
            index (int): Index do item selecionado
        """
        if (index == 1):
            self.selectedVisibility = "CONNECTIONS"
        if (index == 0):
            self.selectedVisibility = "PUBLIC"


    def loadSimpleFields(self):
        """(Postagem Simnples) Adiciona campos necessarios e desabilita os outros radio buttons
        """
        self.radio2.setCheckable(False)
        self.radio3.setCheckable(False)


    def loadArtigoFields(self):
        """(Postagem de Artigo) Adiciona campos necessarios e desabilita os outros radio buttons
        """
        self.radio1.setCheckable(False)
        self.radio2.setCheckable(False)

        self.linkTitle.addWidget(QLabel("Título do Link: "))
        self.linkTitle.addWidget(self.tituloLink)

        self.linkUrl.addWidget(self.lblUrl)
        self.linkUrl.addWidget(self.linkUrlIn)

        self.newLayout.addRow(self.linkTitle)
        self.newLayout.addRow(self.linkTxt)
        self.newLayout.addRow(self.linkUrl)

        if (self.imgAlt.count() > 0):
            self.newLayout.removeItem(self.imgAlt)
        if (self.txtImg.count() > 0):
            self.newLayout.removeItem(self.txtImg)
        if (self.imgImg.count() > 0):
            self.newLayout.removeItem(self.imgImg)


    def loadImagensFields(self):
        """(Postagem com Imagens) Adiciona campos necessarios e desabilita os outros radio buttons
        """
        self.radio1.setCheckable(False)
        self.radio3.setCheckable(False)

        self.imgAlt.addWidget(QLabel("Texto alternativo da imagem: "))
        self.imgAlt.addWidget(self.imgAlttxt)

        self.txtImg.addWidget(QLabel("Texto da Imagem: "))
        self.txtImg.addWidget(self.mediaTxt)

        self.imagem = QLabel(
            "Caminho da Imagem: <span style='font-size: small;color: darkgrey'>com extensão</span>")

        btnCheckImg = QPushButton("Check Image")
        btnCheckImg.adjustSize()
        btnCheckImg.clicked.connect(self.imageCheck)

        self.imgImg.addWidget(self.imagem)
        self.imgImg.addWidget(self.imgPath)
        self.imgImg.addWidget(btnCheckImg)

        self.newLayout.addRow(self.imgAlt)
        self.newLayout.addRow(self.txtImg)
        self.newLayout.addRow(self.imgImg)

        if (self.linkTitle.count() > 0):
            self.newLayout.removeItem(self.linkTitle)
        if (self.linkTxt.count() > 0):
            self.newLayout.removeItem(self.linkTxt)
        if (self.linkUrl.count() > 0):
            self.newLayout.removeItem(self.linkUrl)


    def imageCheck(self):
        """Printa a imagem selecionada na tela
        """
        if (self.imgPath.text() != ""):
            pxImg = QPixmap(self.imgPath.text())
            self.imgLbl.setPixmap(pxImg.scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            self.newLayout.addRow(self.imgLbl)


    def definePostType(self):
        """Define o tipo de popst selecionado
        """
        if (self.radio1.isChecked()):
            self.postTye = "Simples"
        if (self.radio2.isChecked()):
            self.postTye = "Imagem"
        if (self.radio3.isChecked()):
            self.postTye = "Artigo"


    def validationMessages(self):
        """Insere (e remove) as mensagens de validacao dos campos na tela
        """
        if (self.txtPub.toPlainText() == ""):
            self.labelConteudo.setText(
                "Texto da publicação: <span style='color: red'>Preencha o conteudo da postagem!</span>")
        else:
            self.labelConteudo.setText("Texto da publicação: ")

        if (self.postTye == ""):
            self.tipoPubLb.setText(
                "Selecione o tipo de publicação: <span style='color: red'>A seleção é obrigatória!</span>")
        else:
            self.tipoPubLb.setText("Selecione o tipo de publicação: ")

        if (self.postTye == "Artigo"):
            if (self.linkUrlIn.text() == ""):
                self.lblUrl.setText(
                    "URL do Link: <span style='color: red'>O link da publicação é obrigatório!</span>")
        if (self.postTye == "Imagem"):
            if (self.imgPath.text() == ""):
                self.imagem.setText(
                    "Caminho da Imagem: <span style='font-size: small;color: darkgrey'>com extensão</span><span style='color: red'>Obrigatório!</span>")
            else:
                self.imagem.setText(
                    "Caminho da Imagem: <span style='font-size: small;color: darkgrey'>com extensão</span>")


    def validateFields(self):
        """Valida os campos preenchidos e define as variaveis para o request
        """
        self.definePostType()
        self.validationMessages()
        if ((self.txtPub.toPlainText() != "") and (self.postTye == "Artigo" and self.linkUrlIn.text() != "") or (self.postTye == "Imagem" and self.imgPath.text() != "") or (self.postTye == "Simples")):
            self.body = {
                "postType": self.postTye,
                "visibility": self.selectedVisibility,
                "conteudo": self.txtPub.toPlainText(),
                "imageUrl": self.imgPath.text(),
                "altImg": self.imgAlttxt.text(),
                "mediaTxt": self.mediaTxt.text(),
                "tituloLink": self.tituloLink.text(),
                "urlLinkPost": self.linkUrlIn.text(),
            }
            self.aguardeLbl.setText(
                "<b>Aguarde a criação da sua publicação!</b>")
            self.btnPostar.setEnabled(False)
            self.formLayout.addRow(self.aguardeLbl)
        else:
            self.aguardeLbl.setText("Preencha todos os campos necessarios")
            self.body = {}


    def setarAguardeLbl(self, newText):
        """Define o texto da ultima label da tela e
            desabilita o botao de "Potar"

        Args:
            newText (string): Novo texto da label
        """
        self.aguardeLbl.setText(newText)
        self.btnPostar.setEnabled(True)


    def retornarBody(self):
        return self.body

    #endregion