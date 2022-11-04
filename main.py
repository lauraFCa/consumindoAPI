from tkinter import *
from server import *
from readFunc import *

import json

#WARNING nao commitar token
bearerToken = readToken()


root = Tk()
SM = ServerMethods("https://api.linkedin.com/v2", bearerToken)

root.title("Welcome to GeekForGeeks")
root.geometry('350x200')

lbl = Label(root, text="Are you a Geek?")
lbl.grid()

txt = Entry(root, width=10)
txt.grid(column=1, row=0)


def clicked():
    """Acoes que ocorrem quando clica no botao na tela
    """
    x = SM.getPersonBasicInfo()
    print(x["localizedLastName"])
    jsonString = json.dumps(x, indent=1)
    lbl.configure(text = jsonString)


btn = Button(root, text="Click me", fg="red", command=clicked)
btn.grid(column=2, row=0)


root.mainloop()