import csv
import uuid
import os
from datetime import datetime

class Database:

    def __init__(self):
        self.books_file = 'books.csv'
        self.students_file = 'students.csv'
        self.borrowed_file = 'borrowed.csv'
        self.fines_file = 'fines.csv'
        self.librarians_file = 'librarians.csv'
        self.ensure_files_exist()

    def ensure_files_exist(self):
        files_and_headers = [
            (self.books_file, ['id', 'title', 'author', 'copies_available']),
            (self.students_file, ['id', 'name','password']),
            (self.borrowed_file, ['student_id', 'book_id', 'borrow_date', 'return_date']),
            (self.fines_file, ['student_id', 'fine']),
            (self.librarians_file, ['id', 'name', 'password'])
        ]
        for file, headers in files_and_headers:
            try:
                with open(file, 'r'):
                    pass
            except FileNotFoundError:
                with open(file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    
   # ✅ Register Student
    def register_student(self, student_id, name, password):
        if self.student_exists(student_id):
            return False
        with open(self.students_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name, password])
        return True

    # ✅ Authenticate Student
    def authenticate_student(self, student_id, password):
        with open(self.students_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == student_id and row['password'] == password:
                    return True
        return False

    # ✅ Register Librarian
    def register_librarian(self, librarian_id, name, password):
        if self.librarian_exists(librarian_id):
            return False
        with open(self.librarians_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([librarian_id, name, password])
        return True

    # ✅ Authenticate Librarian
    def authenticate_librarian(self, librarian_id, password):
        with open(self.librarians_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == librarian_id and row['password'] == password:
                    return True
        return False

    # ✅ Check if student ID exists
    def student_exists(self, student_id):
        with open(self.students_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == student_id:
                    return True
        return False

    # ✅ Check if librarian ID exists
    def librarian_exists(self, librarian_id):
        if not os.path.exists(self.librarians_file):
            return False
        with open(self.librarians_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == librarian_id:
                    return True
        return False

    def get_available_books(self):
        with open(self.books_file, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader if int(row['copies_available']) > 0]

    def has_already_borrowed(self, student_id, book_id):
        with open(self.borrowed_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['student_id'] == student_id and row['book_id'] == book_id and row['return_date'] == '':
                    return True
        return False

    def borrow_book(self, student_id, book_id):
        if self.has_already_borrowed(student_id, book_id):
            return "You have already borrowed this book."

        books = self.get_available_books()
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return "Book not available."

        if not self.update_book_copies(book_id, -1):
            return "Not enough copies available."

        with open(self.borrowed_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, book_id, datetime.today().strftime('%Y-%m-%d'), ''])

        return "Book borrowed successfully."

    def return_book(self, student_id, book_id):
        updated_rows = []
        fine = 0
        found = False

        with open(self.borrowed_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == student_id and row[1] == book_id and row[3] == '':
                    found = True
                    borrow_date = datetime.strptime(row[2], '%Y-%m-%d')
                    today = datetime.today()
                    days_borrowed = (today - borrow_date).days
                    if days_borrowed > 14:
                        fine = (days_borrowed - 14) * 2
                        self.add_fine(student_id, fine)
                    row[3] = today.strftime('%Y-%m-%d')
                updated_rows.append(row)

        if not found:
            return "No matching borrowed book record found."

        with open(self.borrowed_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        self.update_book_copies(book_id, 1)
        return f"Book returned. Fine: ₹{fine}"

    def get_student_fine(self, student_id):
        with open(self.fines_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['student_id'] == student_id:
                    return row['fine']
        return "0"

    def add_fine(self, student_id, amount):
        fines = {}
        try:
            with open(self.fines_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    fines[row['student_id']] = int(row['fine'])
        except FileNotFoundError:
            pass

        fines[student_id] = fines.get(student_id, 0) + amount

        with open(self.fines_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['student_id', 'fine'])
            for sid, fine in fines.items():
                writer.writerow([sid, fine])

    def deregister_student(self, student_id):
        for file_path in [self.students_file, self.fines_file]:
            with open(file_path, 'r') as file:
                rows = [row for row in csv.reader(file)]
                headers = rows[0]
                rows = [row for row in rows[1:] if row[0] != student_id]

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)
                
    def generate_book_id(self):
        try:
            with open(self.books_file, 'r') as file:
                reader = csv.reader(file)
                next_id = 1
                for i, row in enumerate(reader):
                    if i == 0:
                        continue  # Skip header
                    if row and row[0].isdigit():
                        current_id = int(row[0])
                        if current_id >= next_id:
                            next_id = current_id + 1
            return next_id
        except FileNotFoundError:
            return 1



    def add_book(self, title, author, copies):
        book_id = self.generate_book_id()
    
    # Check if file is empty, and write header if needed
        try:
            write_header = False
            try:
                with open(self.books_file, 'r') as f:
                    if f.readline().strip() == "":
                        write_header = True
            except FileNotFoundError:
                write_header = True

            with open(self.books_file, 'a', newline='') as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(['id', 'title', 'author', 'copies_available'])
                writer.writerow([book_id, title, author, copies])

            return f"Book '{title}' added successfully with ID {book_id}."

        except Exception as e:
            return f"Error adding book: {str(e)}"


    def remove_book(self, book_id):
        with open(self.books_file, 'r') as file:
            books = [row for row in csv.reader(file)]
            headers = books[0]
            books = [row for row in books[1:] if row[0] != book_id]

        with open(self.books_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(books)

        return "Book removed successfully."

    def update_book(self, book_id, new_title=None, new_author=None, new_copies=None):
        updated = False
        with open(self.books_file, 'r') as file:
            books = list(csv.reader(file))
            headers = books[0]
            books_data = books[1:]

        for row in books_data:
            if row[0] == book_id:
                if new_title: row[1] = new_title
                if new_author: row[2] = new_author
                if new_copies is not None: row[3] = str(new_copies)
                updated = True

        with open(self.books_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(books_data)

        return "Book updated successfully." if updated else "Book ID not found."

    def update_book_copies(self, book_id, delta):
        with open(self.books_file, 'r') as file:
            books = list(csv.reader(file))
            headers = books[0]
            books_data = books[1:]

        for row in books_data:
            if row[0] == book_id:
                current_copies = int(row[3])
                if current_copies + delta < 0:
                    return False
                row[3] = str(current_copies + delta)

        with open(self.books_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(books_data)

        return True

    def get_all_students(self):
        with open(self.students_file, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def get_all_borrowed_books(self):
        result = []
        with open(self.borrowed_file, 'r') as file:
            borrowed = list(csv.DictReader(file))

        with open(self.books_file, 'r') as file:
            book_data = {row['id']: row['title'] for row in csv.DictReader(file)}

        for row in borrowed:
            if row['return_date'] == '':
                result.append({
                    'student_id': row['student_id'],
                    'book_id': row['book_id'],
                    'book_title': book_data.get(row['book_id'], 'Unknown')
                })

        return result
