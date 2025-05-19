import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(label, password):
    if not label or not password:
        messagebox.showerror("Error", "Label and Password cannot be empty.")
        return
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (label, password) VALUES (?, ?)", (label, password))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password saved successfully!")

def view_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT label, password FROM passwords")
    records = cursor.fetchall()
    conn.close()

    # Create new window to display records
    view_win = tk.Toplevel(root)
    view_win.title("Saved Passwords")
    view_win.geometry("400x300")
    view_win.configure(bg="black")

    tk.Label(view_win, text="Saved Passwords", font=("Arial", 14, "bold"), fg="red", bg="black").pack(pady=10)

    text_area = tk.Text(view_win, width=50, height=15, fg="red", bg="black", insertbackground="red")
    text_area.pack(padx=10, pady=10)

    if records:
        for rec in records:
            text_area.insert(tk.END, f"Label: {rec[0]}\nPassword: {rec[1]}\n{'-'*40}\n")
    else:
        text_area.insert(tk.END, "No passwords saved yet.")

    text_area.config(state="disabled")  # Read-only

# Password Generation Function
def generate_password():
    try:
        length = int(combo_length.get())
    except ValueError:
        result_label.config(text="Select a valid length.")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    result_label.config(text=password)

def save_password():
    label = entry_label.get().strip()
    password = result_label.cget("text")
    save_to_db(label, password)

# Initialize Database
init_db()

# GUI Setup
root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("400x400")
root.configure(bg="black")

# Add Centered App Title
tk.Label(root, text="Secure Password Generator", fg="red", bg="black", font=("Arial", 20, "bold")).pack(pady=10)

# Label for Service/Account Name
tk.Label(root, text="Label (e.g., Gmail, GitHub):", fg="red", bg="black").pack(pady=5)
entry_label = tk.Entry(root, width=30, fg="red", bg="black", insertbackground="red")
entry_label.pack(pady=5)

# Password Length Selection
tk.Label(root, text="Select Password Length:", fg="red", bg="black").pack(pady=5)
length_options = [str(i) for i in range(4, 33)]
combo_length = ttk.Combobox(root, values=length_options, state="readonly")
combo_length.current(8)  # Default selection: length 12
combo_length.pack(pady=5)

# Adjust Combobox style for dark mode
style = ttk.Style()
style.theme_use('default')
style.configure("TCombobox", fieldbackground="black", background="black", foreground="red")

# Generate Password Button
tk.Button(root, text="Generate Password", command=generate_password, fg="red", bg="black").pack(pady=10)

# Display Generated Password
result_label = tk.Label(root, text="", font=("Courier", 12), fg="red", bg="black", wraplength=300)
result_label.pack(pady=10)

# Save Password Button
tk.Button(root, text="Save to Database", command=save_password, fg="red", bg="black").pack(pady=5)

# View Saved Passwords Button
tk.Button(root, text="View Saved Passwords", command=view_passwords, fg="red", bg="black").pack(pady=10)

root.mainloop()
