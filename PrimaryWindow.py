from tkinter import *

class Janela:
    def __init__(self, master=None):
        self.janela = Tk() #Definição e construção da Janela Inicial
        self.primeiroContainer = Frame(master)
        self.janela.title("Ola")
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close)
        self.janela["background"] = "black"
        self.janela.geometry("180x120+10+20")  #Define as dimensões da nossa Janela Inicial, tais medidas serâo replicadas para as demais janelas

        self.lb = Label(
        self.janela, text="Usuario:", bg="black", fg='white') #Definindo o primeiro campo de texto
        self.lb["font"]=("Arial", "12", "bold")
        self.lb.place(x=15, y=20)  #Define a posição do elemento na janela

        self.ent = Entry(
        self.janela, font="Arial", width=15)  # Criando e definindo o nosso primeiro campo de entrada de dados
        self.ent.place(x=15, y=40)

        self.bt1 = Button(
            self.janela, text="OK", bg="green", fg='white', height=1)  # Definindo o primeiro botão
        self.bt1["font"] = ("Arial", "12", "bold")
        self.bt1["width"] = 6
        self.bt1["command"] = self.lb1_click  # Chama a função que será responsavel por verificar a autenticidade da chave e em seguida depois de validade abrirá a Tela de busca
        self.bt1.place(x=35, y=70)

    def lb1_click(self):  # Será responsável por validar o acesso da chave
        win = Chat(self)
        self.janela.destroy()

    def on_close(self):
        self.janela.destroy()
        root.destroy()


class Chat:
    def __init__(self, master=None):
        self.janela02 = Tk()
        self.janela02.title("Chat")
        self.janela02.protocol("WM_DELETE_WINDOW", self.on_close)
        self.janela02["background"]= "black"
        self.janela02.geometry("500x300+10+20")

        self.lb2 = Label(
        self.janela02, text="         To:", bg="black", fg='white')
        self.lb2["font"] = ("Arial", "12", "bold")
        self.lb2.place(x=280, y=40)

        self.ent = Entry(
        self.janela02, font="Arial", width=12)  # Criando e definindo o nosso primeiro campo de entrada de dados
        self.ent.place(x=350, y=40)

        self.lb3 = Label(
            self.janela02, text="Subject:",bg="black", fg='white')
        self.lb3["font"] = ("Arial", "12", "bold")
        self.lb3.place(x=280, y=80)

        self.ent = Entry(
            self.janela02, font="Arial", width=12)  # Criando e definindo o nosso primeiro campo de entrada de dados
        self.ent.place(x=350, y=80)

        self.lb4 = Label(
            self.janela02, text="Message:", bg="black", fg='white')
        self.lb4["font"] = ("Arial", "12", "bold")
        self.lb4.place(x=280, y=120)

        self.ent = Entry(
            self.janela02, font="Arial", width=20)  # Criando e definindo o nosso primeiro campo de entrada de dados
        self.ent.place(x=278, y=150)

        self.bt6 = Button(
            self.janela02, text="Enviar", bg="green", fg='white', height=1)
        self.bt6["font"] = ("Arial", "12", "bold")
        self.bt6["width"] = 6
        self.bt6.place(x=380, y=250)

        #self.scrollbar = Scrollbar(self.janela02)
        #self.scrollbar.pack(side=RIGHT, fill=Y)
        self.mylist = Listbox(self.janela02)
        #self.mylist = Listbox(self.janela02, yscrollcommand=self.scrollbar.set)
        #self.verificarfato()

        self.mylist["width"]=35
        self.mylist["height"]= 1
        self.mylist.pack(padx=10, pady=20,side=LEFT, fill=BOTH)
        #self.scrollbar.config(command=self.mylist.yview)

    def on_close(self):
        self.janela02.destroy()
        root.destroy()

root = Tk()
root.withdraw()
Janela(root)
root.mainloop()