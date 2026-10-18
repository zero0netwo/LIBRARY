from tkinter import *
from database import get_loans, get_readers, get_available_books, issue_book, return_book
from tkinter import ttk
from tkinter import messagebox

def open_loans_window(parent):
    loans_window = Toplevel(parent)
    loans_window.title("Выдача и возврат книг")
    loans_window.geometry("600x600")

    columns = ("ID", "Reader", "Book", "loan_date", "due_date", "return_date")
    loans_table = ttk.Treeview(loans_window,columns=columns,show="headings")

    loans_table.heading("ID", text="ID")
    loans_table.heading("Reader", text="Читатель")
    loans_table.heading("Book", text="Книга")
    loans_table.heading("loan_date", text="Дата выдачи")
    loans_table.heading("due_date", text="Срок возврата")
    loans_table.heading("return_date", text="Дата возврата")

    loans_table.pack(padx=10,pady=10, fill=BOTH,expand=True)
    def refresh_loans():
        for item in loans_table.get_children():
            loans_table.delete(item)
        loans = get_loans()

        for loan in loans:
            loans_table.insert(
                "",
                END,
                values=(
                    loan[0],
                    loan[1],
                    loan[2],
                    loan[3],
                    loan[4],
                    loan[5]
                )
            )
    def open_issue_book_window():
        reader_map = {
            name: reader_id
            for reader_id, name in get_readers()
        }
        book_map = {
            title: book_id
            for book_id,title in get_available_books()
        }
        issue_window = Toplevel(loans_window)
        issue_window.title("Выдать книгу")
        issue_window.geometry("670x450")

        reader_text = Label(issue_window, text="Читатель")
        reader_text.grid(row=0, column=0, padx=10, pady=10)

        reader_combo = ttk.Combobox(issue_window, values=list(reader_map.keys()), state="readonly", width=35)
        reader_combo.grid(row=0, column=1, padx=10, pady=10)

        book_text = Label(issue_window, text="Книга")
        book_text.grid(row=1, column=0, padx=10, pady=10)

        book_combo = ttk.Combobox(
            issue_window,
            values=list(book_map.keys()),
            state="readonly",
            width=35
        )
        book_combo.grid(row=1, column=1, padx=10, pady=10)

        loan_date_text = Label(issue_window, text="Дата выдачи")
        loan_date_text.grid(row=2, column=0, padx=10, pady=10)

        loan_date_entry = Entry(issue_window, width=38)
        loan_date_entry.grid(row=2, column=1, padx=10, pady=10)

        due_date_text = Label(issue_window, text="Срок возврата")
        due_date_text.grid(row=3, column=0, padx=10, pady=10)

        due_date_entry = Entry(issue_window, width=38)
        due_date_entry.grid(row=3, column=1, padx=10, pady=10)

        def save_issue():
            reader = reader_combo.get()
            book = book_combo.get()
            loan_dates = loan_date_entry.get()
            due_dates = due_date_entry.get()

            if not reader or not book or not loan_dates or not due_dates:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            reader_id = reader_map[reader]
            book_id = book_map[book]

            issue_book(
                reader_id,
                book_id,
                loan_dates,
                due_dates
            )
            messagebox.showinfo("Выдача", "Книга успешно выдана")
            issue_window.destroy()
            refresh_loans()


        save_button = Button(
            issue_window,
            text="Выдать",
            command=save_issue
        )

        save_button.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

    issue_button = Button(
        loans_window,
        text="Выдать книгу",
        command=open_issue_book_window
    )
    issue_button.pack(pady=10)

    def open_return_book_window():
        selected = loans_table.selection()

        if not selected:
            messagebox.showerror(
                "Ошибка",
                "Выберите выдачу"
            )
            return

        item = selected[0]
        values = loans_table.item(item)["values"]

        loan_id = values[0]

        return_window = Toplevel(loans_window)
        return_window.title("Возврат книги")
        return_window.geometry("400x200")

        return_date_text = Label(
            return_window,
            text="Дата возврата"
        )
        return_date_text.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        return_date_entry = Entry(
            return_window,
            width=25
        )
        return_date_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        def save_return():
            return_date = return_date_entry.get()

            if not return_date:
                messagebox.showerror(
                    "Ошибка",
                    "Введите дату возврата"
                )
                return
            result = return_book(loan_id, return_date)

            if result:
                messagebox.showinfo(
                    "Возврат",
                    "Книга успешно возвращена"
                )
                return_window.destroy()
                refresh_loans()
            else:
                messagebox.showerror(
                    "Ошибка",
                    "Книга уже была возвращена"
                )

        save_return_button = Button(
            return_window,
            text="Вернуть",
            command=save_return
        )

        save_return_button.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=20
        )

    return_button = Button(
            loans_window,
            text="Вернуть книгу",
            command=open_return_book_window
        )

    return_button.pack(pady=10)

    refresh_loans()