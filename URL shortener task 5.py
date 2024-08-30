import tkinter as tk
from tkinter import messagebox
import sqlite3
import string
import random

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT UNIQUE
    )
    ''')
    conn.commit()
    conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def insert_url(original_url, short_url):
    conn = get_db_connection()
    conn.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)',
                 (original_url, short_url))
    conn.commit()
    conn.close()

def get_original_url(short_url):
    conn = get_db_connection()
    url_data = conn.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    conn.close()
    return url_data['original_url'] if url_data else None

# GUI setup
def shorten_url():
    original_url = url_entry.get()
    if not original_url:
        messagebox.showerror("Error", "Please enter a URL to shorten")
        return

    short_url = generate_short_url()
    insert_url(original_url, short_url)

    result_label.config(text=f"Short URL: {short_url}", fg="green")

def redirect_url():
    short_url = redirect_entry.get()
    if not short_url:
        messagebox.showerror("Error", "Please enter a short URL")
        return

    original_url = get_original_url(short_url)
    if original_url:
        messagebox.showinfo("Redirect", f"Original URL: {original_url}")
    else:
        messagebox.showerror("Error", "Short URL not found")

# Initialize the database
create_table()

# Main application window
app = tk.Tk()
app.title("URL Shortener")
app.geometry("400x300")
app.configure(bg="#f0f0f0")  # Light grey background

# URL Shortener Frame
frame = tk.Frame(app, bg="#d9ead3")  # Light green background
frame.pack(pady=20, padx=10, fill="x")

url_label = tk.Label(frame, text="Enter URL to shorten:", bg="#d9ead3", font=("Arial", 12))
url_label.grid(row=0, column=0, padx=10, pady=10)

url_entry = tk.Entry(frame, width=30, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=10, pady=10)

shorten_button = tk.Button(frame, text="Shorten", command=shorten_url, bg="#b6d7a8", fg="black", font=("Arial", 10, "bold"))
shorten_button.grid(row=0, column=2, padx=10, pady=10)

result_label = tk.Label(frame, text="", bg="#d9ead3", font=("Arial", 12, "italic"))
result_label.grid(row=1, column=0, columnspan=3, pady=10)

# URL Redirect Frame
redirect_frame = tk.Frame(app, bg="#cfe2f3")  # Light blue background
redirect_frame.pack(pady=20, padx=10, fill="x")

redirect_label = tk.Label(redirect_frame, text="Enter short URL to redirect:", bg="#cfe2f3", font=("Arial", 12))
redirect_label.grid(row=0, column=0, padx=10, pady=10)

redirect_entry = tk.Entry(redirect_frame, width=30, font=("Arial", 12))
redirect_entry.grid(row=0, column=1, padx=10, pady=10)

redirect_button = tk.Button(redirect_frame, text="Redirect", command=redirect_url, bg="#9fc5e8", fg="black", font=("Arial", 10, "bold"))
redirect_button.grid(row=0, column=2, padx=10, pady=10)

# Run the application
app.mainloop()
