import requests
import json


class ServerMethods:

    def __init__(self, URL, token):
        self.URL = URL
        self.token = token
        self.userId = self.getPersonId()
        self.asset, self.uploadUrl = "", ""


    def getPersonFullInfo(self):
        """Obtem dados completos do usuario autenticado com o token

        Returns:
            json: informacoes sobre o usuario no formato Json
        """
        authHeader = {"Authorization": "Bearer " + self.token}
        extraInfo = {
            "projection": "(id,firstName,lastName,profilePicture(displayImage~:playableStreams))"}
        r = requests.get(url=self.URL + "/me", headers=authHeader, params=extraInfo)
        return r.json()


    def getPersonBasicInfo(self):
        """Obtem dados basicos do usuario autenticado com o token

        Returns:
            json: informacoes sobre o usuario no formato Json
        """
        authHeader = {"Authorization": "Bearer " + self.token}
        r = requests.get(url=self.URL + "/me", headers=authHeader)
        if r.status_code == 200:
            return r.json()
        else:
            return 'Request Fail'


    def getPersonId(self):
        """Obtem o identificador da pessoa autenticada com o token

        Returns:
            string: identificador do usuario
        """
        resp = self.getPersonBasicInfo()
        resp = json.dumps(resp, indent=4)
        resp = json.loads(resp)
        return resp["id"]


    def postSimple(self, conteudo, visibility):
        """Realiza uma postagem de conteudo no perfil do usuario autenticado

        Args:
            conteudo (string): Conteudo principal do post
            visibility (string): Publico ou Apenas para conexoes
        Returns:
            r: Resposta completa da requisicao
        """
        authHeader = {"Authorization": "Bearer " + self.token}
        postBody = {
            "author": "urn:li:person:"+str(self.userId),
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": conteudo
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        r = requests.post(self.URL + "/ugcPosts", headers=authHeader, json=postBody)
        if (r.status_code != 201):
            print("Erro: " + r.text)
            return "Erro: " + str(r.text)
        else:
            jsonSaida = r.json()
            return jsonSaida["id"]


    def postArticle(self, conteudo, visibility, articleText, articleUrl, linkText="link text"):
        """Realiza uma postagem de conteudo no perfil do usuario autenticado

        Args:
            conteudo (string): Conteudo principal do post
            visibility (string): Publico ou Apenas para conexoes
            articleText (string): Texto principal do link - manchete
            articleUrl (string): URL que direciona a outra pagina
            linkText (string): Texto aternativo para a URL
        Returns:
            r: Resposta completa da requisicao
        """
        authHeader = {"Authorization": "Bearer " + self.token}
        postBody = {
            "author": "urn:li:person:"+str(self.userId),
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
                                "text": articleText
                            },
                            "originalUrl": articleUrl,
                            "title": {
                                "text": linkText
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        r = requests.post(self.URL + "/ugcPosts", headers=authHeader, json=postBody)
        if (r.status_code != 201):
            return "Erro: " + r.text
        else:
            jsonSaida = r.json()
            return jsonSaida["id"]


    def registrarImagem(self):
        """Registra a imagem para ser postada

        Returns:
            string: Retorno do request (sucesso ou falha)
        """
        authHeader = {"Authorization": "Bearer " + self.token}
        postBody = {
            "registerUploadRequest": {
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "owner": "urn:li:person:" + str(self.userId),
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        extraInfo = {"action": "registerUpload"}
        r = requests.post(self.URL + "/assets", params=extraInfo, headers=authHeader, json=postBody)
        jsonRetorno = r.json()
        jsonRetorno = json.dumps(jsonRetorno)
        jsonRetorno = json.loads(jsonRetorno)
        if (r.status_code == 200):
            value = jsonRetorno["value"]
            self.asset = value["asset"]
            self.uploadUrl = jsonRetorno["value"]["uploadMechanism"][
                "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
            return "Success"
        else:
            return "registrarImagem Erro: " + str(r.status_code) + " - " + jsonRetorno["message"]


    def postImagem(self, imgPath):
        """Posta a imagem local no espaco reservado com o registro

        Args:
            imgPath (string): caminho relativo da imagem a ser enviada

        Returns:
            string: Retorno do request (sucesso ou falha)
        """
        r = self.registrarImagem()
        if ("Erro" in r):
            return r
        else:
            authHeader = {"Authorization": "Bearer " + self.token}
            with open(imgPath, 'rb') as f:
                data = f.read()
            r = requests.put(self.uploadUrl, headers=authHeader, data=data)
            if (r.status_code == 201):
                return "Success"
            else:
                return "Erro: " + str(r.status_code) + r.text


    def postComImagem(self, imgPath, conteudo, visibility, altImg, mediaTxt):
        """Faz o POST de uma publicacao com Imagem

        Args:
            imgPath (string): Caminho local do arquivo de imagem
            conteudo (string): Conteudo do post (texto)
            visibility (string): Visibiliade do post (publico ou para conexoes)
            altImg (string): Texto alternativo da imagem postada
            mediaTxt (string): Descricao da imagem

        Returns:
            string: Mensagem de erro ou o ID da publicacao, em caso de sucesso
        """
        authHeader = {"Authorization": "Bearer " + self.token, 'Content-Type': 'application/json'}
        saida = self.postImagem(imgPath)
        if ("Erro" in saida):
            return saida
        else:
            postBody = {
                "author": "urn:li:person:"+str(self.userId),
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": conteudo
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [{"status": "READY",
                                   "description": {
                                       "text": altImg
                                   },
                                   "media": self.asset,
                                   "title": {
                                       "text": mediaTxt
                                   }
                                   }]}
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            print('BODY - ', json.dumps(postBody, indent=4))
            r = requests.post(self.URL + "/ugcPosts", headers=authHeader, json=postBody)
            if (r.status_code != 201):
                return "Erro: " + r.text
            else:
                jsonSaida = r.json()
                return jsonSaida["id"]
