import tkinter as tk
from tkinter import messagebox
from database import Database

print("main_helper loaded")
print(dir())

db = Database()

# Utility function to close window after action
def close_window(window):
    window.destroy()

def student_register(root):
    window = tk.Toplevel(root)
    window.title("Student Registration")
    window.geometry("300x300")

    tk.Label(window, text="Student ID").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()

    tk.Label(window, text="Name").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Password").pack()
    pass_entry = tk.Entry(window, show="*")
    pass_entry.pack()

    def register():
        sid = id_entry.get().strip()
        name = name_entry.get().strip()
        password = pass_entry.get().strip()

        if db.register_student(sid, name, password):
            messagebox.showinfo("Success", "Student registered successfully!")
            close_window(window)
        else:
            messagebox.showerror("Error", "Student ID already exists.")

    tk.Button(window, text="Register", command=register).pack(pady=10)

def student_login(root):
    window = tk.Toplevel(root)
    window.title("Student Login")
    window.geometry("300x250")

    tk.Label(window, text="Student ID").pack()
    id_entry = tk.Entry(window)
    id_entry.pack()

    tk.Label(window, text="Password").pack()
    pass_entry = tk.Entry(window, show="*")
    pass_entry.pack()

    def login():
        sid = id_entry.get().strip()
        password = pass_entry.get().strip()

        if db.authenticate_student(sid, password):
            messagebox.showinfo("Success", "Login successful!")
            close_window(window)
            student_dashboard(root, sid)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    tk.Button(window, text="Login", command=login).pack(pady=10)

def librarian_register(root):
    window = tk.Toplevel(root)
    window.title("Librarian Registration")
    window.geometry("300x300")

    tk.Label(window, text="Librarian ID").pack()
    lid_entry = tk.Entry(window)
    lid_entry.pack()

    tk.Label(window, text="Name").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Password").pack()
    pass_entry = tk.Entry(window, show="*")
    pass_entry.pack()

    def register():
        lid = lid_entry.get().strip()
        name = name_entry.get().strip()
        password = pass_entry.get().strip()

        if db.register_librarian(lid, name, password):
            messagebox.showinfo("Success", "Librarian registered successfully!")
            close_window(window)
        else:
            messagebox.showerror("Error", "Librarian ID already exists.")

    tk.Button(window, text="Register", command=register).pack(pady=10)

def librarian_login(root):
    window = tk.Toplevel(root)
    window.title("Librarian Login")
    window.geometry("300x250")

    tk.Label(window, text="Librarian ID").pack()
    lid_entry = tk.Entry(window)
    lid_entry.pack()

    tk.Label(window, text="Password").pack()
    pass_entry = tk.Entry(window, show="*")
    pass_entry.pack()

    def login():
        lid = lid_entry.get().strip()
        password = pass_entry.get().strip()

        if db.authenticate_librarian(lid, password):
            messagebox.showinfo("Success", "Login successful!")
            close_window(window)
            librarian_panel(root, lid)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    tk.Button(window, text="Login", command=login).pack(pady=10)

# ---------------- Student Dashboard ----------------
def student_dashboard(root, student_id):
    window = tk.Toplevel(root)
    window.title(f"Student Dashboard - {student_id}")
    window.geometry("400x400")

    def view_books():
        books = db.get_available_books()
        book_list = "\n".join([f"{b['id']}: {b['title']} by {b['author']}" for b in books])
        messagebox.showinfo("Available Books", book_list or "No books available.")

    def borrow_book():
        book_id = simple_input("Enter Book ID to Borrow")
        if book_id:
            msg = db.borrow_book(student_id, book_id.strip())
            messagebox.showinfo("Borrow Book", msg)

    def return_book():
        book_id = simple_input("Enter Book ID to Return")
        if book_id:
            msg = db.return_book(student_id, book_id.strip())
            messagebox.showinfo("Return Book", msg)

    def check_fine():
        fine = db.get_student_fine(student_id)
        messagebox.showinfo("Fine", f"Total Fine: ₹{fine}")

    def deregister():
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to deregister?")
        if confirm:
            db.deregister_student(student_id)
            messagebox.showinfo("Deregister", "You have been deregistered.")
            window.destroy()

    def simple_input(prompt):
        input_win = tk.Toplevel(window)
        input_win.title(prompt)
        tk.Label(input_win, text=prompt).pack()
        entry = tk.Entry(input_win)
        entry.pack()

        result = {}

        def submit():
            result['value'] = entry.get()
            input_win.destroy()

        tk.Button(input_win, text="Submit", command=submit).pack()
        window.wait_window(input_win)
        return result.get('value')

    tk.Button(window, text="View Available Books", command=view_books).pack(pady=10)
    tk.Button(window, text="Borrow Book", command=borrow_book).pack(pady=10)
    tk.Button(window, text="Return Book", command=return_book).pack(pady=10)
    tk.Button(window, text="Check Fine", command=check_fine).pack(pady=10)
    tk.Button(window, text="Deregister", command=deregister).pack(pady=10)

# ---------------- Librarian Panel ----------------
def librarian_panel(root, librarian_id):
    window = tk.Toplevel(root)
    window.title(f"Librarian Panel - {librarian_id}")
    window.geometry("400x400")

    def add_book():
        title = simple_input("Enter Book Title")
        author = simple_input("Enter Author")
        copies = simple_input("Enter No. of Copies")
        if title and author and copies:
            try:
                msg = db.add_book(title.strip(), author.strip(), int(copies.strip()))
                messagebox.showinfo("Add Book", msg)
            except ValueError:
                messagebox.showerror("Error", "Copies must be an integer.")

    def remove_book():
        book_id = simple_input("Enter Book ID to Remove")
        if book_id:
            msg = db.remove_book(book_id.strip())
            messagebox.showinfo("Remove Book", msg)

    def update_book():
        book_id = simple_input("Enter Book ID to Update")
        if not book_id: return
        title = simple_input("New Title (Leave blank to skip)")
        author = simple_input("New Author (Leave blank to skip)")
        copies = simple_input("New No. of Copies (Leave blank to skip)")

        try:
            msg = db.update_book(
                book_id.strip(),
                title.strip() if title else None,
                author.strip() if author else None,
                int(copies.strip()) if copies else None
            )
            messagebox.showinfo("Update Book", msg)
        except ValueError:
            messagebox.showerror("Error", "Copies must be an integer.")

    def view_students():
        students = db.get_all_students()
        info = "\n".join([f"{s['id']}: {s['name']}" for s in students])
        messagebox.showinfo("Students", info or "No students found.")

    def view_borrowed():
        borrowed = db.get_all_borrowed_books()
        info = "\n".join([f"{b['student_id']} borrowed {b['book_title']} (Book ID: {b['book_id']})" for b in borrowed])
        messagebox.showinfo("Borrowed Books", info or "No borrowed books.")

    def simple_input(prompt):
        input_win = tk.Toplevel(window)
        input_win.title(prompt)
        tk.Label(input_win, text=prompt).pack()
        entry = tk.Entry(input_win)
        entry.pack()

        result = {}

        def submit():
            result['value'] = entry.get()
            input_win.destroy()

        tk.Button(input_win, text="Submit", command=submit).pack()
        window.wait_window(input_win)
        return result.get('value')

    tk.Button(window, text="Add Book", command=add_book).pack(pady=10)
    tk.Button(window, text="Remove Book", command=remove_book).pack(pady=10)
    tk.Button(window, text="Update Book Info", command=update_book).pack(pady=10)
    tk.Button(window, text="View All Students", command=view_students).pack(pady=10)
    tk.Button(window, text="View Borrowed Books", command=view_borrowed).pack(pady=10)
