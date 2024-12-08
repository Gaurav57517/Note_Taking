import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from fpdf import FPDF

# Database setup
conn = sqlite3.connect('notes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
conn.commit()

# GUI setup
root = tk.Tk()
root.title("Note-Taking App by Gaurav")
root.geometry("600x500")

# Functions
def save_note():
    title = title_entry.get()
    content = text_area.get("1.0", tk.END)
    if title and content:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        messagebox.showinfo("Note Saved", "Your note has been saved successfully!")
    else:
        messagebox.showwarning("Empty Fields", "Both title and content are required.")

def load_note():
    title = title_entry.get()
    if title:
        c.execute("SELECT content FROM notes WHERE title=?", (title,))
        note = c.fetchone()
        if note:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, note[0])
        else:
            messagebox.showwarning("Note Not Found", "No note found with that title.")
    else:
        messagebox.showwarning("Title Required", "Please enter a title to load a note.")

def export_note():
    content = text_area.get("1.0", tk.END)
    if content.strip():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        
        # Save as PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Export Success", f"Note exported to {file_path}")
    else:
        messagebox.showwarning("Empty Content", "Cannot export an empty note.")

def import_note():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, content)

# GUI 
title_label = tk.Label(root, text="Title:")
title_label.pack(pady=5)

title_entry = tk.Entry(root, width=50)
title_entry.pack(pady=5)

text_area = tk.Text(root, wrap="word", width=60, height=20)
text_area.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="Save Note", command=save_note)
save_button.grid(row=0, column=0, padx=10)

load_button = tk.Button(button_frame, text="Load Note", command=load_note)
load_button.grid(row=0, column=1, padx=10)

export_button = tk.Button(button_frame, text="Export Note as PDF", command=export_note)
export_button.grid(row=0, column=2, padx=10)

import_button = tk.Button(button_frame, text="Import Note", command=import_note)
import_button.grid(row=0, column=3, padx=10)

root.mainloop()
conn.close()
