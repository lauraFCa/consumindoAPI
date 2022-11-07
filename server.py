import requests

class ServerMethods:

    def __init__(self, URL, token):
        self.URL = URL
        self.token = token


    def getPersonFullInfo(self):
        """Obtem dados completos do usuario autenticado com o token

        Returns:
            json: informacoes sobre o usuario no formato Json
        """
        authHeader = {"Authorization": "Bearer "+ self.token}
        extraInfo = {"projection": "(id,firstName,lastName,profilePicture(displayImage~:playableStreams))"}
        r = requests.get(url = self.URL + "/me", headers=authHeader, params=extraInfo)
        return r.json()


    def getPersonBasicInfo(self):
        """Obtem dados basicos do usuario autenticado com o token

        Returns:
            json: informacoes sobre o usuario no formato Json
        """
        authHeader = {"Authorization": "Bearer "+ self.token}
        r = requests.get(url = self.URL + "/me", headers=authHeader)
        if r.status_code == 200:
            return r.json()
        else:
            return 'Request Fail'


    def getPersonId(self):
        """Obtem o identificador da pessoa autenticada com o token

        Returns:
            string: identificador
        """
        resp = self.getPersonBasicInfo()
        return resp
    

    def requestPOST(self, conteudo, descricao, url, tituloUrl):
        """Realiza uma postagem de conteudo no perfil do usuario autenticado

        Args:
            conteudo (string): Conteudo principal do post
            descricao (string): Continuacao do conteudo - breve descricao
            url (string): URL para redirecionar a alguma outra pagina
            tituloUrl (string): Titulo da URL adicionada

        Returns:
            json: Corpo da resposta (contem apenas o ID da publicacao)
        """
        authHeader = {"Authorization": "Bearer "+ self.token}
        personId = self.getPersonId()
        postBody = {
                "author": "urn:li:person:"+personId,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": conteudo
                        },
                        "shareMediaCategory": "ARTICLE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": descricao
                                },
                                "originalUrl": url,
                                "title": {
                                    "text": tituloUrl
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
                }
        }
        r = requests.post(url = self.URL + "/ugcPosts", headers=authHeader, data=postBody)
        return r.json()

