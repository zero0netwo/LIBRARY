from tkinter import *
from database import connection
from auth import authenticate_user,get_guest_user
from UI.main_window import open_main_window

def auth_user():
    auth_window = Tk()
    auth_window.title("Авторизация")
    auth_window.geometry("420x220")

    #Label

    title_text = Label(auth_window, text="Авторизация")
    title_text.grid(column=0, row=0, columnspan=2, padx=20, pady=15)

    email_text = Label(auth_window, text="email")
    email_text.grid(column=0, row=1, padx=10, pady=8, sticky="e")

    password_text = Label(auth_window, text="Пароль")
    password_text.grid(column=0, row=2, padx=10, pady=8, sticky="e")

    #Entry
    email_field = Entry(auth_window, width=30)
    email_field.grid(column=1,row=1, padx=10, pady=8)

    password_field = Entry(auth_window, width=30, show="*")
    password_field.grid(column=1, row=2, padx=10, pady=8)

    def Enter_BT():
        username = email_field.get()
        user_password = password_field.get()

        user = authenticate_user(username, user_password)

        if user:
            open_main_window(auth_window, user)
        else:
            print("Неверный логин или пароль")

    def guest_BT():
        user = get_guest_user()
        open_main_window(auth_window, user)

    Enter = Button(auth_window, text="Войти", command=Enter_BT)
    Enter.grid(column=0, row=3, padx=10, pady=15)

    guest_button = Button(auth_window, text="Войти как гость", command=guest_BT)
    guest_button.grid(column=1,row=3,padx=10,pady=15)


    auth_window.mainloop()



