"""Flask web app for managing books and authors in a library."""
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
from sqlalchemy.exc import IntegrityError
from stdnum import isbn
from stdnum.exceptions import ValidationError

app = Flask(__name__)

folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, "data", "library.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)

with app.app_context():
    db.create_all()


def get_book_cover(isbn):
    """Get a book cover using ISBN."""
    url = "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg"
    return url


@app.route('/')
def show_home():
    """Show the main page with all the books."""
    sort = request.args.get('sort', 'title')
    search = request.args.get('search', '').strip()

    books = Book.query.join(Author)

    if search:
        search = f"%{search}%"
        books = books.filter(
            db.or_(
                Book.title.ilike(search),
                Author.name.ilike(search)
            )
        )

    if sort == 'title':
        books = books.order_by(Book.title)
    elif sort == 'author':
        books = books.order_by(Author.name)
    elif sort == 'year':
        books = books.order_by(Book.publication_year)

    all_books = books.all()
    for book in all_books:
        book.cover_url = get_book_cover(book.isbn)

    return render_template('home.html', books=all_books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_new_author():
    """Add a new author to the library."""
    if request.method == 'POST':
        name = request.form['name'].strip()
        birth = request.form['birth_date']
        death = request.form['date_of_death']

        birth_date = datetime.strptime(birth, '%Y-%m-%d').date()
        if death:
            death_date = datetime.strptime(death, '%Y-%m-%d').date()
        else:
            death_date = None

        # Check for duplicate author name
        authors = Author.query.all()
        author_names = [author.name.lower().strip() for author in authors]
        if name.lower().strip() in author_names:
            flash(f'An author with the name "{name}" already exists.', 'error')
            return render_template('add_author.html')

        author = Author(
            name=name.strip(),
            birth_date=birth_date,
            date_of_death=death_date
        )

        try:
            db.session.add(author)
            db.session.commit()
            flash('Author added successfully', 'success')
            return redirect(url_for('show_home'))
        except IntegrityError:
            db.session.rollback()
            flash(f'An author with the name "{name}" already exists.', 'error')
            return render_template('add_author.html')

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_new_book():
    """Add a new book to the library."""
    if request.method == 'POST':
        isbn_number = request.form['isbn'].strip()
        title = request.form['title'].strip()       
        year = int(request.form['publication_year'])
        author_id = int(request.form['author_id'])

       #validate isbn 
        try:
            isbn.validate(isbn_number)
        except ValidationError:
            flash('Invalid ISBN. Please enter a valid 10 or 13-digit number. 13-digit ISBNs must start with 978 or 979.', 'error')
            return render_template('add_book.html', authors=Author.query.all())


        # Check for duplicate book ISBN
        #get all book isbn and check if the isbn is already in the list
        books = Book.query.all()
        book_isbns = [book.isbn.strip() for book in books]
        if isbn_number in book_isbns:
            flash(f'A book with ISBN "{isbn_number}" already exists in the library.', 'error')
            return render_template('add_book.html', authors=Author.query.all())

        
        book = Book(
            isbn=isbn_number,
            title=title,
            publication_year=year,
            author_id=author_id
        )
        
        try:
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully', 'success')
            return redirect(url_for('show_home'))
        except IntegrityError:
            db.session.rollback()
            flash(f'A book with ISBN "{isbn_number}" already exists in the library.', 'error')
            return render_template('add_book.html', authors=Author.query.all())

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book from the library."""
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()
        flash(f'Book "{book.title}" and author "{author.name}" have been deleted.')
    else:
        flash(f'Book "{book.title}" has been deleted.')

    return redirect(url_for('show_home'))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Show details about a specific book."""
    book = Book.query.get_or_404(book_id)
    book.cover_url = get_book_cover(book.isbn)
    return render_template('book_detail.html', book=book)


@app.route('/author/<int:author_id>')
def author_detail(author_id):
    """Show details about a specific author."""
    author = Author.query.get_or_404(author_id)
    for book in author.books:
        book.cover_url = get_book_cover(book.isbn)
    return render_template('author_detail.html', author=author)


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """Delete an author and all their books."""
    author = Author.query.get_or_404(author_id)
    name = author.name
    book_count = len(author.books)

    db.session.delete(author)
    db.session.commit()

    flash(f'Author "{name}" and their {book_count} book(s) have been deleted.')
    return redirect(url_for('show_home'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)