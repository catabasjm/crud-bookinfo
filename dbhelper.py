'''
    dbhelper
'''
from mysql.connector import connect

# Function to connect to the MySQL database
def dbconnect():
    return connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='bookdb'
    )

# Function to execute a SELECT query and return the results as a list of dictionaries
def getprocess(sql: str, params: tuple = ()) -> list:
    db = dbconnect()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# Function to execute an INSERT, UPDATE, or DELETE query
def postprocess(sql: str, params: tuple = ()) -> bool:
    db = dbconnect()
    cursor = db.cursor()
    cursor.execute(sql, params)
    db.commit()
    success = cursor.rowcount > 0
    cursor.close()
    db.close()
    return success

# Function to get all records from a specified table
def getall_record(table: str) -> list:
    sql = f"SELECT * FROM `{table}`"
    return getprocess(sql)

# Function to add a new book with all required fields as parameters
def addnewbook(isbn: str, title: str, author: str, copyright: str, edition: str, price: float, qty: int, total: float) -> bool:
    sql = """
    INSERT INTO books (isbn, title, author, copyright, edition, price, qty, total)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (isbn, title, author, copyright, edition, price, qty, total)
    return postprocess(sql, params)
    
def get_book_by_isbn(isbn):
    sql = "SELECT * FROM books WHERE isbn = %s"
    result = getprocess(sql, (isbn,))
    return result[0] if result else None  # Return the first item if it exists, else None

def update_book(isbn, title, author, copyright, edition, price, qty, total):
    sql = """
    UPDATE books SET title = %s, author = %s, copyright = %s, edition = %s, price = %s, qty = %s, total = %s
    WHERE isbn = %s
    """
    return postprocess(sql, (title, author, copyright, edition, price, qty, total, isbn))

def delete_book(isbn):
    sql = "DELETE FROM books WHERE isbn = %s"
    return postprocess(sql, (isbn,))

