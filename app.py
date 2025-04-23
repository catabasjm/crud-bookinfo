'''
    Catabas, Jhana Marie D.
    BSIT 3A
    7:30 - 10:00 AM TTH
'''
from flask import Flask, render_template, request, redirect, flash, url_for
from dbhelper import addnewbook, getall_record, get_book_by_isbn, update_book, delete_book

app = Flask(__name__)
app.secret_key = "!@#@!#!"

@app.route("/")
def index():
    return redirect(url_for("booklist"))

# Route to display the list of books
@app.route("/booklist")
def booklist():
    try:
        books = getall_record("books")
    except Exception as e:
        flash(f"Error loading books: {e}")
        books = []
    return render_template("index.html", books=books, pagetitle='Book Information')

# Route to add or update a book
@app.route("/addbook", methods=['POST'])
def addbook():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    copyright = request.form['copyright']
    edition = request.form['edition']
    
    try:
        price = float(request.form['price'])  # Convert price to float
    except ValueError:
        flash("Error: Invalid price format. Please enter a valid number.", "error")
        return redirect(url_for("booklist"))

    qty = int(request.form['qty'])
    total = price * qty

    if request.form.get("editbook"):  # Edit mode
        ok = update_book(isbn, title, author, copyright, edition, price, qty, total)
        message = "Book updated successfully!" if ok else "Error updating book."
    else:  # Add new book
        # Check if ISBN already exists
        existing_book = get_book_by_isbn(isbn)
        if existing_book:
            flash("Error: A book with this ISBN already exists! Please use a different ISBN.", "error")
            return redirect(url_for("booklist"))
        else:
            ok = addnewbook(isbn, title, author, copyright, edition, price, qty, total)
            message = "Book added successfully!" if ok else "Error adding book."

    flash(message)
    return redirect(url_for("booklist"))


# Route to edit a book - loads data into the form
@app.route("/editbook/<isbn>")
def edit_book(isbn):
    book = get_book_by_isbn(isbn)
    return render_template("index.html", book=book, books=getall_record("books"), pagetitle='Book Information')

# Route to delete a book (renamed to avoid conflict with dbhelper function)
@app.route("/deletebook/<isbn>")
def delete_book_route(isbn):
    if delete_book(isbn):
        flash("Book deleted successfully!")
    else:
        flash("Error deleting book.")
    return redirect(url_for("booklist"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
