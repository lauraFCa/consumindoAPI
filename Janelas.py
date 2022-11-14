import json
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget

from Layouts import Layouts
from server import ServerMethods

windowsSize = 640, 500
ly = Layouts()
url = "https://api.linkedin.com/v2"


class MainWindow(QWidget):

    def __init__(self):
        """Janela principal
        """
        super().__init__()
        self.setMinimumSize(windowsSize[0], windowsSize[1])
        ly.setPrincipalLayout(self, self.checkToken)
        self.token = ''

    def checkToken(self):
        """Recupera o valor do token inserido
        """
        self.token = ly.returnToken()
        if (self.token == '' or len(self.token) < 100):
            erro = "<span style='color: red; font-weight: 700'>Preencha um token válido!</span>"
            ly.setMsgErro(erro)
        else:
            self.optionW = OptionsWindow(self.token)
            self.optionW.setMinimumSize(windowsSize[0], windowsSize[1])
            self.optionW.show()
            self.hide()


class OptionsWindow(QWidget):

    def __init__(self, tk):
        """Janela com opcoes de acao
        """
        super().__init__()
        self.token = tk

        ly.setOpcoesLayout(self, self.openDadosPessoais,
                           self.openPublicacoes, self.token, self.voltar)

    def openDadosPessoais(self):
        self.personal = DadosPessoais(self.token)
        self.personal.setMinimumSize(windowsSize[0], windowsSize[1])
        self.personal.show()
        self.hide()

    def openPublicacoes(self):
        self.public = CriarPublicacoes(self.token)
        self.public.setMinimumSize(windowsSize[0], windowsSize[1])
        self.public.show()
        self.hide()

    def voltar(self):
        self.mw = MainWindow()
        self.mw.setMinimumSize(windowsSize[0], windowsSize[1])
        self.mw.show()
        self.close()


class DadosPessoais(QWidget):

    def __init__(self, tk):
        """Janela com opcoes de acao
        """
        super().__init__()
        self.setMinimumSize(windowsSize[0], windowsSize[1])
        self.labelsInicializados = self.inicializarCampos()
        ly.setDadosLayout(self, self.getDadosPessoais, self.getMaisDados,
                          self.labelsInicializados[0], self.labelsInicializados[1], self.printJason, self.voltar)
        self.token, self.resp, self.jsonCompleto = tk, 0, ""
        self.sm = ServerMethods(url, self.token)

    def inicializarCampos(self):
        labelsDados, labelsMaisDados = [], []
        camposDados, camposMaisDados = 9, 9

        for i in range(camposDados):
            lb = QLabel("", self)
            lb.setWordWrap(True)
            labelsDados.append(lb)

        for i in range(camposMaisDados):
            lb1 = QLabel("", self)
            lb1.setWordWrap(True)
            labelsMaisDados.append(lb1)

        return labelsDados, labelsMaisDados

    def getDadosPessoais(self):
        self.infosP = self.sm.getPersonBasicInfo()
        self.infosPstr = json.dumps(self.infosP, indent=4)
        self.infosP = json.loads(self.infosPstr)
        self.userId = self.infosP["id"]
        self.resp = 1
        ly.setarValores1NaTela(self.infosP)

    def getMaisDados(self):
        self.maisInfos = self.sm.getPersonFullInfo()
        self.maisInfosStr = json.dumps(self.maisInfos, indent=4)
        self.maisInfos = json.loads(self.maisInfosStr)
        self.userId = self.maisInfos["id"]
        self.resp = 2
        ly.setarValores2NaTela(self.maisInfos)

    def printJason(self):
        if (self.resp == 1):
            self.jsonCompleto = self.infosPstr
        if (self.resp == 2):
            self.jsonCompleto = self.maisInfosStr

        ly.setarJsonNaTela(self.jsonCompleto)

    def getUserId(self):
        return self.userId

    def voltar(self):
        self.optWin = OptionsWindow(self.token)
        self.optWin.setMinimumSize(windowsSize[0], windowsSize[1])
        self.optWin.show()
        self.close()


class CriarPublicacoes(QWidget):

    def __init__(self, tk):
        """Janela com opcoes de acao
        """
        super().__init__()
        self.setMinimumSize(windowsSize[0], windowsSize[1])
        #self.labelsInicializados = self.inicializarCampos()
        ly.setarPubLayout(self, self.getDataAndPost, self.voltar)
        self.token, self.resp, self.jsonCompleto = tk, 0, ""
        self.sm = ServerMethods(url, self.token)


    def getDataAndPost(self):
        ly.validateFields()
        self.conteudosFormulario = ly.retornarBody()
        if (len(self.conteudosFormulario) > 0):
            tipo = self.conteudosFormulario["postType"]
            if (tipo == "Simples"):
                self.makeSimplePost()
            if (tipo == "Artigo"):
                self.makeArticlePost()
            if (tipo == "Imagem"):
                self.makeImagePost()


    def makeSimplePost(self):
        conteudo = self.conteudosFormulario["conteudo"]
        visivel = self.conteudosFormulario["visibility"]
        resposta = self.sm.postSimple(conteudo, visivel)
        if ("Erro" in resposta):
                ly.setarAguardeLbl(
                    "<span style='font-weight: 800; font-size: medium'>Algo deu errado com a requisição!</span>")
        else:
            linkPost = "https://www.linkedin.com/embed/feed/update/" + \
                str(resposta)
            ly.setarAguardeLbl(
                f"<span style='font-weight: 800; font-size: medium'>Post realizado com sucesso!<br><a href='{linkPost}'>Clique aqui para visualizar!</a></span>")


    def makeArticlePost(self):
        conteudo = self.conteudosFormulario["conteudo"]
        visivel = self.conteudosFormulario["visibility"]
        tituloLink = self.conteudosFormulario["tituloLink"]
        urlLinkPost = self.conteudosFormulario["urlLinkPost"]
        resposta = self.sm.postArticle(conteudo, visivel, tituloLink, urlLinkPost)
        if ("Erro" in resposta):
            ly.setarAguardeLbl(
                "<span style='font-weight: 800; font-size: medium'>Algo deu errado com a requisição!</span>")
        else:
            linkPost = "https://www.linkedin.com/embed/feed/update/" + \
                str(resposta)
            ly.setarAguardeLbl(
                f"<span style='font-weight: 800; font-size: medium'>Post realizado com sucesso!<br><a href='{linkPost}'>Clique aqui para visualizar!</a></span>")


    def makeImagePost(self):
        conteudo = self.conteudosFormulario["conteudo"]
        visivel = self.conteudosFormulario["visibility"]
        imgUrl = self.conteudosFormulario["imageUrl"]
        altIm = self.conteudosFormulario["altImg"]
        mediaTxt = self.conteudosFormulario["mediaTxt"]
        resposta = self.sm.postComImagem(
            imgUrl, conteudo, visivel, altIm, mediaTxt)
        if ("Erro" in resposta):
            ly.setarAguardeLbl(
                "<span style='font-weight: 800; font-size: medium'>Algo deu errado com a requisição!</span>")
        else:
            linkPost = "https://www.linkedin.com/embed/feed/update/" + \
                str(resposta)
            ly.setarAguardeLbl(
                f"<span style='font-weight: 800; font-size: medium'>Post realizado com sucesso!<br><a href='{linkPost}'>Clique aqui para visualizar!</a></span>")


    def voltar(self):
        self.optWin = OptionsWindow(self.token)
        self.optWin.setMinimumSize(windowsSize[0], windowsSize[1])
        self.optWin.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(app.exec())
