from tkinter import *
from UI.books_window import open_books_window
from UI.loans_window import open_loans_window
from database import get_roles, add_user
from tkinter import ttk
from tkinter import messagebox

def open_main_window(auth_window,user):
    auth_window.withdraw()

    main_window = Toplevel()
    main_window.title("Главное окно")
    main_window.geometry("700x450")
    main_window.resizable(False, False)

    user_id = user[0]
    username = user[1]
    role_id = user[2]
    full_name = user[3]
    role_name = user[4]

    info = Label(main_window, text=f"{full_name} | роль: {role_name}", font=("Arial", 11))
    info.place(relx=1.0, x=-15, y=15, anchor="ne")

    title = Label(main_window, text="Библиотека")
    title.pack(pady=55)

    catalog_button = Button(main_window, text="Каталог книг", width=28, command=lambda: open_books_window(main_window, role_name))
    catalog_button.pack(pady=10)

    if role_name == "administrator" or role_name == "librarian":
        loan_wnd_button = Button(main_window, text="Открыть окно ", command=lambda: open_loans_window(main_window))
        loan_wnd_button.pack(pady=10)

    def open_add_user_window():
        add_user_window = Toplevel(main_window)
        add_user_window.title("Добавить пользователя")
        add_user_window.geometry("500x350")

        roles = get_roles()

        role_map = {
            name: role_id
            for role_id, name in roles
        }
        username_label = Label(
            add_user_window,
            text="Логин"
        )
        username_label.grid(row=0, column=0, padx=10, pady=10)

        username_entry = Entry(
            add_user_window,
            width=30
        )
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = Label(
            add_user_window,
            text="Пароль"
        )
        password_label.grid(row=1, column=0, padx=10, pady=10)

        password_entry = Entry(
            add_user_window,
            width=30
        )
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        full_name_label = Label(
            add_user_window,
            text="ФИО"
        )
        full_name_label.grid(row=2, column=0, padx=10, pady=10)

        full_name_entry = Entry(
            add_user_window,
            width=30
        )
        full_name_entry.grid(row=2, column=1, padx=10, pady=10)

        role_label = Label(
            add_user_window,
            text="Роль"
        )
        role_label.grid(row=3, column=0, padx=10, pady=10)

        role_combo = ttk.Combobox(
            add_user_window,
            values=list(role_map.keys()),
            state="readonly",
            width=27
        )
        role_combo.grid(row=3, column=1, padx=10, pady=10)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            full_name = full_name_entry.get()
            role = role_combo.get()

            if not username or not password or not full_name or not role:
                messagebox.showerror(
                    "Ошибка",
                    "Заполните все поля"
                )
                return

            role_id = role_map[role]

            add_user(
                username,
                password,
                role_id,
                full_name
            )

            messagebox.showinfo(
                "Добавление пользователя",
                "Пользователь успешно добавлен"
            )

            add_user_window.destroy()

        save_user_button = Button(
            add_user_window,
            text="Добавить пользователя",
            command=save_user
        )

        save_user_button.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

    if role_name == "administrator":
        add_user_button = Button(
            main_window,
            text="Добавить пользователя",
            width=28,
            command=open_add_user_window
        )

        add_user_button.pack(pady=10)