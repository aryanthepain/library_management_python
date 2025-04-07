import tkinter as tk
from main_helper import (
    student_register,
    student_login,
    librarian_register,
    librarian_login
)

def main():
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("400x400")

    tk.Label(root, text="Welcome to the Library System", font=("Arial", 16)).pack(pady=20)

    # Student Section
    student_frame = tk.LabelFrame(root, text="Student", padx=10, pady=10)
    student_frame.pack(pady=10)

    tk.Button(student_frame, text="Register", width=20, command=lambda: student_register(root)).pack(pady=5)
    tk.Button(student_frame, text="Login", width=20, command=lambda: student_login(root)).pack(pady=5)

    # Librarian Section
    librarian_frame = tk.LabelFrame(root, text="Librarian", padx=10, pady=10)
    librarian_frame.pack(pady=10)

    tk.Button(librarian_frame, text="Register", width=20, command=lambda: librarian_register(root)).pack(pady=5)
    tk.Button(librarian_frame, text="Login", width=20, command=lambda: librarian_login(root)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
