import socket
import threading
import tkinter
from tkinter import *

from ChatClient import Client


class Gui:
    """inits the client, open login window. Must start the server before"""

    def __init__(self):
        self.client = Client()
        self.client.connect()

        """Login Window, calls the main window by "login" button via lambda"""
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(0, 0)
        self.login.geometry("240x100")
        self.login.columnconfigure(0, weight=1)
        self.login.columnconfigure(1, weight=3)
        self.pls = Label(self.login, text="Please login to continue", justify=CENTER)
        self.pls.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
        self.labelName = Label(self.login, text="Name: ")
        self.labelName.grid(column=0, row=1, sticky=tkinter.W, padx=5, pady=5)
        self.entryName = Entry(self.login)
        self.entryName.grid(column=1, row=1, sticky=tkinter.E, padx=5, pady=5)
        self.entryName.focus()
        self.login = Button(self.login, text="login", command=lambda: self.main_window(self.entryName.get()))
        print(self.name)
        self.client.name = self.name
        self.login.grid(column=1, row=3, sticky=tkinter.E, padx=5, pady=5)
        self.Window.mainloop()

    def main_window(self, name):
        """main chat window, first closes the login window"""
        self.login.destroy()
        self.name = name

        """Window configuration"""
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#CD6090")
        self.labelHead = Label(self.Window, bg="#17202A", fg="#CD6090", text=self.name, pady=5)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        self.labelBottom = Label(self.Window, bg="#CD6090", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()
        self.buttonMsg = Button(self.labelBottom, text="Send", width=15, bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get(), self.name))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def sendButton(self, msg, name):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.client.send(msg, name)
        self.entryMsg.delete(0, END)

    # def receive(self):
    #     while True:
    #         try:
    #             message = self.client.recv(1024).decode()
    #             if message == 'NAME':
    #                 self.client.client_sock.send(self.name)
    #             else:
    #
    #                 self.textCons.config(state=NORMAL)
    #                 self.textCons.insert(END,
    #                                      message + "\n\n")
    #
    #                 self.textCons.config(state=DISABLED)
    #                 self.textCons.see(END)
    #         except:
    #
    #             print("An error occured!")
    #             self.client.close()
    #             break

    # def sendMessage(self):
    #     """here must be the connection between gui and client"""
    #     self.textCons.config(state=DISABLED)
    #     while True:
    #          message = (f"{self.name}: {self.msg}")


if __name__ == '__main__':
    g = Gui()

