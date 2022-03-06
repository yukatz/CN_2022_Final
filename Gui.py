from tkinter import ttk
from ChatClient import Client
import tkinter



class GUI:
    def __init__(self):
        self.client = Client()


    def login_win(self):
        login = tkinter.Tk()
        login.geometry("240x100")
        login.title('Login')
        login.resizable(0, 0)
        """Grid size"""
        login.columnconfigure(0, weight=1)
        login.columnconfigure(1, weight=3)
        """User pointer"""
        username_label = ttk.Label(login, text="Username:")
        username_label.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
        """Name entry line"""
        username_entry = tkinter.Entry(login)
        username_entry.grid(column=1, row=0, sticky=tkinter.E, padx=5, pady=5)
        """login button"""
        login_button = ttk.Button(login, text="Login", command = self.chat_window, )
        login_button.grid(column=1, row=3, sticky=tkinter.E, padx=5, pady=5)
        login.mainloop()

    def chat_window(self):
        window = tkinter.Tk()
        window.title('A&Y Chatroom')
        window.resizable(width=False, height=False)
        window.configure(width = 470, height = 550, bg = "#8B0A50")

        frm_messages = tkinter.Frame(master=window)
        frm_clients = tkinter.Frame(master=window, bg = "#FF1493")

        scrollbar = tkinter.Scrollbar(master=frm_messages)
        messages = tkinter.Listbox(master=frm_messages,yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=False)
        messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)



        frm_messages.grid(row=0, column=0, columnspan=1,  sticky="nsew")
        frm_clients.grid(row=0, column=1, columnspan=1,rowspan=1, sticky="nsew")

        frm_entry = tkinter.Frame(master=window)
        text_input = tkinter.Entry(master=frm_entry)
        text_input.pack(fill=tkinter.BOTH, expand=True)
        text_input.bind("<Return>")
        text_input.insert(0, "Your message here.")

        btn_send = tkinter.Button(
            master=window,
            text='Send',

        )

        frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
        btn_send.grid(row=1, column=1, pady=10, sticky="ew")

        window.rowconfigure(0, minsize=500, weight=1)
        window.rowconfigure(1, minsize=50, weight=0)
        window.columnconfigure(0, minsize=500, weight=1)
        window.columnconfigure(1, minsize=200, weight=0)

        window.mainloop()










if __name__ == '__main__':

    gui = GUI()

