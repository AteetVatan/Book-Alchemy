"""Database models for the library application."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """An author who writes books."""
    __tablename__ = 'author'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        """Return a string representation of the author."""
        return 'Author: ' + self.name
    
    def __str__(self):
        """string representation of the author class."""
        if self.date_of_death:
            return self.name + ' (' + str(self.birth_date.year) + '-' + str(self.date_of_death.year) + ')'
        else:
            return self.name + ' (' + str(self.birth_date.year) + '-Living)'

class Book(db.Model):
    """A book written by an author."""
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    def __repr__(self):
        """Return a string representation of the book."""
        return 'Book: ' + self.title
    
    def __str__(self):
        """string representation of the book class."""
        return self.title + ' (' + str(self.publication_year) + ')'
