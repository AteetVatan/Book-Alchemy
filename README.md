# Book-Alchemy 📚

A Flask-based library management system that allows you to manage books and authors. The application uses SQLAlchemy for database management.

## Features

- **Book Management**
  - Add, view, and delete books
  - Automatic book cover fetching from Open Library
  - Search books by title or author
  - Sort books by title, author, or publication year

- **Author Management**
  - Add and manage authors with birth/death dates
  - View all books by an author
  - Cascade deletion (deleting an author removes their books)
  - Author detail pages with complete bibliography

- **User Interface**
  - Clean, modern design
  - Responsive layout
  - Intuitive navigation
  - Confirmation dialogs for destructive actions
  - Flash messages for operation feedback

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Book-Alchemy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Database Structure

### Author Table
- id (Primary Key)
- name
- birth_date
- date_of_death (optional)

### Book Table
- id (Primary Key)
- isbn (13 digits)
- title
- publication_year
- author_id (Foreign Key)

## Dependencies

- Flask (3.0.0)
- Flask-SQLAlchemy (3.1.1)
- SQLAlchemy (2.0.23)
- Werkzeug (3.0.1)
- Other dependencies listed in requirements.txt

## Development

### Project Structure
```
Book-Alchemy/
├── app.py              # Main application file
├── data_models.py      # Database models
├── requirements.txt    # Project dependencies
├── populate_library.sql# Sample data SQL script
├── data/              # Database directory
│   └── library.sqlite
└── templates/         # HTML templates
    ├── home.html
    ├── add_book.html
    ├── add_author.html
    ├── book_detail.html
    └── author_detail.html
```

### Features Implementation

1. **Book Cover Display**
   - Automatic fetching from Open Library
   - Graceful fallback to book emoji
   - Responsive image sizing

2. **Search and Sort**
   - Real-time search functionality
   - Multiple sort options
   - Clean URL parameters

3. **Data Management**
   - SQLAlchemy ORM
   - Cascade deletions
   - Data validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Open Library for their book covers API
- Flask and SQLAlchemy communities
- All contributors to the project 