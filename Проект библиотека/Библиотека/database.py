import mysql.connector
from mysql.connector import Error, IntegrityError
from config import DB_CONFIG

def connection():
    try:
        connect = mysql.connector.connect(**DB_CONFIG)
        return connect
    except Error as error:
        print(f"Ошибка подключения: {error} ")
        return None

def find_user(username, password):
    connect_db = connection()
    cursor = connect_db.cursor()
    query = """ 
        SELECT 
            users.user_id,
            users.username,
            users.role_id,
            users.full_name,
            roles.name
        FROM users JOIN roles ON users.role_id = roles.role_id WHERE users.username = %s AND users.password=%s
            """

    try:
        cursor.execute(query, (username,password))
        return cursor.fetchone()
    finally:
        cursor.close()
        connect_db.close()


#def get_roles():
    #connect = connection()
   # if conn

def get_books(search_text="", availability="Все книги", sort_option="Название А-Я"):
    connect_db = connection()
    cursor = connect_db.cursor()
    query = """ 
        SELECT 
            books.book_id,
            books.title,
            CONCAT(authors.first_name, ' ' , authors.last_name) AS author_name, 
            genres.name AS genre_name,
            books.publication_year,
            books.price,
            books.quantity,
            books.image_path
        FROM books
        JOIN authors ON books.author_id = authors.author_id
        JOIN genres ON books.genre_id = genres.genre_id
        WHERE 1 = 1
    """

    params = []

    if search_text:
        query += """
            AND (
                books.title LIKE %s 
                OR CONCAT(authors.first_name, " ", authors.last_name) LIKE %s
                OR genres.name LIKE %s 
            )
        """
        search_value = f"%{search_text}%"
        params.extend([search_value, search_value, search_value])

    if availability == "В наличии":
        query += " AND books.quantity >= 4"
    elif availability == "Заканчивается":
        query += " AND books.quantity BETWEEN 1 AND 3"
    elif availability == "Нет в наличии":
        query += " AND books.quantity = 0"

    sort_map ={
        "Название А-Я": "books.title ASC",
        "Название Я-А": "books.title DESC",
        "Год ↑": "books.publication_year ASC",
        "Год ↓": "books.publication_year DESC",
        "Цена ↑": "books.price ASC",
        "Цена ↓": "books.price DESC"

    }

    query += " ORDER BY " + sort_map.get(sort_option, "books.title ASC")

    try:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        connect_db.close()

def get_authors():
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        cursor.execute(""" 
            SELECT
                authors.author_id,
                CONCAT(authors.first_name, ' ', authors.last_name)
            FROM authors
            ORDER BY authors.last_name, authors.first_name
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connect_db.close()

def get_genres():
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        cursor.execute("""
            SELECT
                genre_id,
                name
            FROM genres
            ORDER BY name
        """)
        return cursor.fetchall()

    finally:
        cursor.close()
        connect_db.close()

def add_book(title, author_id, genre_id, publication_year, price, quantity, image_path):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            INSERT INTO books(
                title,
                author_id,
                genre_id,
                publication_year,
                price,
                quantity,
                image_path
            ) VALUES(%s,%s,%s,%s,%s,%s,%s)
        
        """
        params = (
            title,
            author_id,
            genre_id,
            publication_year,
            price,
            quantity,
            image_path
        )
        cursor.execute(query, params)
        connect_db.commit()

    finally:
        cursor.close()
        connect_db.close()

def get_book_by_id(book_id):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            SELECT
                b.book_id,
                b.title,
                b.author_id,
                b.genre_id,
                b.publication_year,
                b.price,
                b.quantity,
                b.image_path
            FROM books AS b
            WHERE book_id = %s
        
        """
        cursor.execute(query, (book_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        connect_db.close()

def update_book(book_id, title_valid, author_id, genre_id, year_valid, price_valid, quantity_valid, image_edit):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            UPDATE books
            SET 
                title = %s,
                author_id = %s,
                genre_id = %s,
                publication_year = %s,
                price = %s,
                quantity = %s,
                image_path = %s
            WHERE book_id = %s
        """
        cursor.execute(query,(title_valid, author_id, genre_id, year_valid, price_valid, quantity_valid, image_edit, book_id))
        connect_db.commit()

    finally:
        cursor.close()
        connect_db.close()


def has_active_loan(book_id):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            SELECT 
                loan_id
            FROM loans
            WHERE book_id = %s
            AND return_date IS NULL
        
        """
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()

        return result is not None

    finally:
        cursor.close()
        connect_db.close()



def delete_book(book_id):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
        DELETE FROM books WHERE book_id = %s
        
        """
        cursor.execute(query, (book_id,))
        connect_db.commit()

    finally:
        cursor.close()
        connect_db.close()

def get_loans():
    connect_db = connection()
    cursor = connect_db.cursor()
    try:
        query = """
            SELECT
                loans.loan_id,
                readers.full_name,
                books.title,
                loans.loan_date,
                loans.due_date,
                loans.return_date
            FROM loans
            JOIN readers ON loans.reader_id = readers.reader_id
            JOIN books ON loans.book_id = books.book_id
            ORDER BY loans.loan_date DESC  
            """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    finally:
        cursor.close()
        connect_db.close()

def get_readers():
    connect_db = connection()
    cursor = connect_db.cursor()
    try:
        query = """
            SELECT
                reader_id,
                full_name
            FROM readers
            ORDER BY full_name
            """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connect_db.close()

def get_available_books():
    connect_db = connection()
    cursor = connect_db.cursor()
    try:
        query = """
            SELECT 
                book_id,
                title
            FROM books
            WHERE quantity > 0
            ORDER BY title """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connect_db.close()


def issue_book(reader_id, book_id, loan_date, due_date):
    connect_db = connection()
    cursor = connect_db.cursor()
    try:
        query_loan = """
            INSERT INTO loans(
                reader_id,
                book_id,
                loan_date,
                due_date,
                return_date
            )
            VALUES(%s, %s,%s,%s, NULL)
        """
        cursor.execute(query_loan,(reader_id,book_id,loan_date,due_date))
        query_book = """
            UPDATE books
            SET quantity = quantity - 1
            WHERE book_id = %s
        """
        cursor.execute(query_book,(book_id,))
        connect_db.commit()

    finally:
        cursor.close()
        connect_db.close()

def return_book(loan_id, return_date):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query_find = """
            SELECT book_id
            FROM loans
            WHERE loan_id = %s
            AND return_date IS NULL
        """

        cursor.execute(query_find, (loan_id,))
        result = cursor.fetchone()

        if result is None:
            return False

        book_id = result[0]

        query_loan = """
            UPDATE loans
            SET return_date = %s
            WHERE loan_id = %s
        """

        cursor.execute(
            query_loan,
            (return_date, loan_id)
        )

        query_book = """
            UPDATE books
            SET quantity = quantity + 1
            WHERE book_id = %s
        """

        cursor.execute(query_book, (book_id,))

        connect_db.commit()

        return True

    finally:
        cursor.close()
        connect_db.close()

def get_roles():
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            SELECT
                role_id,
                name
            FROM roles
            ORDER BY role_id
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        connect_db.close()


def add_user(username, password, role_id, full_name):
    connect_db = connection()
    cursor = connect_db.cursor()

    try:
        query = """
            INSERT INTO users (
                username,
                password,
                role_id,
                full_name
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                username,
                password,
                role_id,
                full_name
            )
        )

        connect_db.commit()

    finally:
        cursor.close()
        connect_db.close()