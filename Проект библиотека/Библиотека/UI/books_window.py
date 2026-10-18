from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from database import get_books, get_genres, get_authors, add_book, get_book_by_id, update_book, has_active_loan, delete_book


def open_books_window(parent, role_name):
    books_window = Toplevel(parent)
    books_window.title("Просмотр каталога")
    books_window.geometry("1180x720")

    title = Label(books_window, text="Каталог книг", font=("Arial", 22, "bold"))
    title.pack(pady=10)

    search_entry = Entry(books_window, width=30)
    search_entry.pack(pady=5)

    filter_combo = ttk.Combobox(books_window, values=("Все книги","В наличии", "Заканчивается", "Нет в наличии"),state="readonly",width=25 )
    filter_combo.pack(pady=5)
    filter_combo.set("Все книги")

    sort_combo = ttk.Combobox(books_window, values=("Название А-Я", "Название Я-А", "Год ↑", "Год ↓", "Цена ↑", "Цена ↓"), state="readonly", width=25)
    sort_combo.pack(pady=5)
    sort_combo.set("Название А-Я")

    admin_frame = Frame(books_window)
    admin_frame.pack(pady=5)


    columns = ('id', 'title', 'author', 'genre', 'year', 'price', 'quantity', 'status')
    books_table = ttk.Treeview(books_window, columns=columns, show="tree headings")

    style = ttk.Style()
    style.configure("Treeview", rowheight=90)

    project_path = Path(__file__).resolve().parent.parent

    placeholder_path = project_path / "images" / "placeholder.png"

    books_table.heading("id", text="ID")
    books_table.heading("title", text="Название")
    books_table.heading("author", text="Автор")
    books_table.heading("genre", text="Жанр")
    books_table.heading("year", text="Год")
    books_table.heading("price", text="Цена")
    books_table.heading("quantity", text="Количество")
    books_table.heading("status", text="Статус")
    books_table.heading("#0", text="Обложка")
    books_table.column("#0", width=90, stretch=False, anchor="center")

    books_table.pack(padx=10, pady=10, fill=BOTH, expand=True)

    image_refs = []


    def refresh_books(event=None):
        for item in books_table.get_children():
            books_table.delete(item)

        image_refs.clear()

        books = get_books(
            search_text=search_entry.get(),
            availability=filter_combo.get(),
            sort_option=sort_combo.get()
        )
        for book in books:
            if book[6] == 0:
                status = "Нет в наличии"
            elif book[6] <= 3:
                status = "Заканчивается"

            else:
                status = "В наличии"
            book_image = load_look_image(book[7])

            image_refs.append(book_image)
            

            books_table.insert(
                "",
                END,
                image=book_image,
                values=(
                    book[0],
                    book[1],
                    book[2],
                    book[3],
                    book[4],
                    book[5],
                    book[6],
                    status
                )
            )

    search_entry.bind("<KeyRelease>", refresh_books)
    filter_combo.bind("<<ComboboxSelected>>", refresh_books)
    sort_combo.bind("<<ComboboxSelected>>", refresh_books)

    def load_look_image(image_path):
        if image_path:
            path = Path(image_path)

            if not path.is_absolute():
                path = project_path / path

            if not path.exists():
                path = placeholder_path

        else:
            path = placeholder_path


        try:
            image = PhotoImage(file=str(path))

        except TclError:
            image = PhotoImage(file=str(placeholder_path))

        image = image.subsample(8, 8)
        return image

    def open_add_book_window():
        add_book_window = Toplevel(books_window)
        add_book_window.title("Добавление книги")
        add_book_window.geometry("450x450")

        title_text = Label(add_book_window, text="Заголовок")
        title_text.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        title_field = Entry(add_book_window, width=40)
        title_field.grid(row=0, column=1, padx=10, pady=10, sticky="e")


        authors = get_authors()
        author_map = {
            name: author_id
            for author_id, name in authors

        }

        author_text = Label(add_book_window, text="Автор")
        author_text.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        author_combo = ttk.Combobox(add_book_window, values=list(author_map.keys()), state="readonly", width=40)
        author_combo.grid(row=1, column=1, padx=10, pady=10)

        genres_text = Label(add_book_window, text="Жанр")
        genres_text.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        genres = get_genres()
        genres_map = {
            name: genre_id
            for genre_id, name in genres

        }

        genres_combo = ttk.Combobox(add_book_window, values=list(genres_map.keys()), state="readonly", width=40)
        genres_combo.grid(row=2, column=1, padx=10, pady=10)

        year_text = Label(add_book_window, text="Год")
        year_text.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        year_field = Entry(add_book_window, width=40)
        year_field.grid(row=3, column=1, padx=10, pady=10)

        price_text = Label(add_book_window, text="Цена")
        price_text.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        price_field = Entry(add_book_window, width=40)
        price_field.grid(row=4, column=1, padx=10, pady=10)

        quantity_text = Label(add_book_window, text="Количество")
        quantity_text.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        quantity_field = Entry(add_book_window, width=40)
        quantity_field.grid(row=5, column=1, padx=10, pady=10)

        image_text = Label(add_book_window, text="Изображение")
        image_text.grid(row=6,column=0, padx=10, pady=10, sticky="e")

        image_field = Entry(add_book_window, width=40)
        image_field.grid(row=6, column=1, padx=10, pady=10)

        def choose_image():
            file_path = filedialog.askopenfilename(
                title="Выберите изображения",
                filetypes=[
                    ("PNG", "*.png"),
                    ("Все файлы", "*.*")
                ]
            )
            if file_path:
                image_field.delete(0, END)
                image_field.insert(0, file_path)

        image_button = Button(add_book_window, text="Выбрать", command=choose_image)
        image_button.grid(row=6, column=2, padx=5, pady=10)

        def save_book():
            title = title_field.get()

            author_name = author_combo.get()

            # проверка автора

            author_valid = author_name.strip()
            if not author_valid:
                messagebox.showerror("Ошибка", "Выберите автора")
                return

            author_id = author_map[author_name]


            genre_name = genres_combo.get()

            # проверка жанра

            genre_valid = genre_name.strip()
            if not genre_valid:
                messagebox.showerror("Ошибка", "Выберите жанр")
                return

            genre_id = genres_map[genre_name]

            year = year_field.get()
            price = price_field.get()
            quantity = quantity_field.get()
            image = image_field.get()

            # проверка заголовка
            title_valid = title.strip()
            if not title_valid:
                messagebox.showerror("Ошибка", "Название не может быть пустым")
                return

            # проверка цены

            try:
                price_valid = float(price)
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом")
                return

            if price_valid < 0:
                messagebox.showerror("Ошибка", "Цена не должна быть отрицательной")
                return

            # проверка даты

            try:
                year_int = int(year)
            except ValueError:
                messagebox.showerror("Ошибка", "Год должен быть числом")
                return

            if year_int <= 0:
                messagebox.showerror("Ошибка", "Не валидное значение")
                return

            # проверка количества

            try:
                quantity_valid = int(quantity)
            except ValueError:
                messagebox.showerror("Ошибка", "Должно быть число или цифра")
                return

            if quantity_valid < 0:
                messagebox.showerror("Ошибка", "Количество не может быть отрицательным")
                return

            # проверка картинки

            if image:
                try:
                    image_valid = PhotoImage(file=image)
                except TclError:
                    messagebox.showerror("Ошибка", "Файл изображения поврежден или имеет неподдерживаемый формат")
                    return

            add_book(
                title_valid,
                author_id,
                genre_id,
                year_int,
                price_valid,
                quantity_valid,
                image
            )
            messagebox.showinfo("Добавление книги", "Книга добевлена")

            add_book_window.destroy()
            refresh_books()

        save_button = Button(add_book_window, text="Добавить", command=save_book)
        save_button.grid(row=7, column=0, columnspan=3, pady=20)

    if role_name == "administrator":
        add_button = Button(admin_frame, text="Добавить книгу", command=open_add_book_window)
        add_button.pack(pady=5)


        def get_values_from_table():


            get_values = books_table.selection()

            if get_values:

                for item in get_values:
                    items = books_table.item(item)
                    values = items['values']
                    book_id = values[0]
                    print("ID книги: ", book_id)

                    book = get_book_by_id(book_id)
                    print(book)

                    open_edit_window(book)

            else:
                messagebox.showerror("Ошибка", "Выберите поле")

        def open_edit_window(book):
            edit_window = Toplevel(books_window)
            edit_window.title("Окно редактирования")
            edit_window.geometry("450x450")

            title_text = Label(edit_window, text="Заголовок")
            title_text.grid(row=0, column=0, padx=10, pady=10, sticky="e")

            title_field = Entry(edit_window, width=40)
            title_field.insert(0, book[1])
            title_field.grid(row=0, column=1, padx=10, pady=10)

            authors = get_authors()
            author_map = {
                author_id: name
                for author_id, name in authors

            }

            author_text = Label(edit_window, text="Автор")
            author_text.grid(row=1, column=0, padx=10, pady=10, sticky="e")

            author_field = ttk.Combobox(edit_window, values=list(author_map.values()), state="readonly", width=40)
            author_field.set(author_map[book[2]])
            author_field.grid(row=1, column=1, padx=10, pady=10)

            genres_text = Label(edit_window, text="Жанр")
            genres_text.grid(row=2, column=0, padx=10, pady=10, sticky="e")

            genres = get_genres()
            genres_map = {
                genre_id: name
                for genre_id, name in genres

            }

            genres_field = ttk.Combobox(edit_window, values=list(genres_map.values()), state="readonly", width=40)
            genres_field.set(genres_map[book[3]])
            genres_field.grid(row=2, column=1, padx=10, pady=10)

            year_text = Label(edit_window, text="Год")
            year_text.grid(row=3, column=0, padx=10, pady=10, sticky="e")

            year_field = Entry(edit_window, width=40)
            year_field.insert(0, book[4])
            year_field.grid(row=3, column=1, padx=10, pady=10)

            price_text = Label(edit_window, text="Цена")
            price_text.grid(row=4, column=0, padx=10, pady=10, sticky="e")

            price_field = Entry(edit_window, width=40)
            price_field.insert(0, book[5])
            price_field.grid(row=4, column=1, padx=10, pady=10)

            quantity_text = Label(edit_window, text="Количество")
            quantity_text.grid(row=5, column=0, padx=10, pady=10, sticky="e")

            quantity_field = Entry(edit_window, width=40)
            quantity_field.insert(0, book[6])
            quantity_field.grid(row=5, column=1, padx=10, pady=10)

            image_text = Label(edit_window, text="Изображение")
            image_text.grid(row=6, column=0, padx=10, pady=10, sticky="e")

            image_field = Entry(edit_window, width=40)
            image_field.grid(row=6, column=1, padx=10, pady=10)
            image_path = image_field

            if book[7]:
                image_field.insert(0, book[7])
            else:
                print("Пустое поле")


            def save_upload():
                title_edit = title_field.get()

                title_valid = title_edit.strip()

                if not title_valid:
                    messagebox.showerror("Ошибка", "Добавьте заголовок")
                    return

                author_edit = author_field.get()

                author_valid = author_edit.strip()

                author_id_map = {
                    name: author_id
                    for author_id, name in authors
                }

                if not author_valid:
                    messagebox.showerror("Ошибка", "Добавьте автора")
                    return

                author_id = author_id_map[author_valid]


                genre_edit = genres_field.get()
                genre_valid = genre_edit.strip()

                genre_id_map = {
                    name: genre_id
                    for genre_id, name in genres
                }

                if not genre_valid:
                    messagebox.showerror("Ошибка", "Добавьте жанр")
                    return

                genre_id = genre_id_map[genre_valid]

                year_edit = year_field.get()

                try:
                    year_valid = int(year_edit)
                except ValueError:
                    messagebox.showerror("Ошибка", "Год должен быть числом")
                    return

                if year_valid <= 0:
                    messagebox.showerror("Ошибка", "Год не может быть меньше или равен 0")
                    return



                price_edit = price_field.get()
                try:
                    price_valid = float(price_edit)
                except ValueError:
                    messagebox.showerror("Ошибка", "Цена должна быть числом или десятичной")
                    return
                if price_valid < 0:
                    messagebox.showerror("Ошибка", "Цена не  может быть меньше 0")
                    return

                quantity_edit = quantity_field.get()
                try:
                    quantity_valid = int(quantity_edit)
                except ValueError:
                    messagebox.showerror("Ошибка", "Количество должно быть числом")
                    return
                if quantity_valid < 0:
                    messagebox.showerror("Ошибка", "Количество не  может быть меньше 0")
                    return



                image_edit = image_field.get()
                if image_edit:
                    try:
                        image_valid = PhotoImage(file=image_edit)
                    except TclError:
                        messagebox.showerror("Ошибка", "Файл поврежден или формат не поддерживается")
                        return

                update_book(book[0], title_valid, author_id, genre_id, year_valid, price_valid, quantity_valid, image_edit)
                messagebox.showinfo("Редактирование", "Книга успешно обновлена")
                edit_window.destroy()
                refresh_books()

            save_edit_button = Button(edit_window, text='Сохранить изменения', command=save_upload)
            save_edit_button.grid(row=9, column=1, padx=10, pady=10)




        button_edit = Button(admin_frame, text="Редактировать", command=get_values_from_table)
        button_edit.pack(pady=5)


        def delete_book_from_window():
            get_items = books_table.selection()

            if get_items:
                for item in get_items:
                    items = books_table.item(item)
                    values = items["values"]
                    book_id = values[0]
                    print("ID книги", book_id)


                    good = messagebox.askyesno(title = "Подтверждение", message="Подтвердить удаление?")
                    if good:
                        if has_active_loan(book_id):
                            messagebox.showerror("Ошибка", "Книга не может быть удалена: она сейчас выдана")
                            return

                        delete_book(book_id)
                        messagebox.showinfo("Результат", "Книга удалена")

                        refresh_books()

                    else:
                        messagebox.showinfo("Результат", "Операция отклонена")


            else:
                messagebox.showerror("Ошибка", "Выберите поле для удаления")

        delete_button = Button(admin_frame, text="Удалить книгу", command= delete_book_from_window)
        delete_button.pack(pady=5)



    refresh_books()

