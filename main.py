import os
import shutil
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from organizer import organize_files
from database import( get_history, clear_history,get_last_record)


# -----------------------------
# Browse Folder
# -----------------------------
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)


# -----------------------------
# Organize Files
# -----------------------------
def organize():
    folder = folder_path.get()

    if folder == "":
        messagebox.showerror("Error", "Please select a folder.")
        return

    status_text.set("Organizing files...")
    progress["value"] = 20
    root.update_idletasks()

    organize_files(folder)

    progress["value"] = 100
    root.update_idletasks()

    status_text.set("Files organized successfully!")

    messagebox.showinfo(
        "Success",
        "Files organized successfully!"
    )

    progress["value"] = 0


# -----------------------------
# View History
# -----------------------------
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("File History")
    history_window.geometry("900x400")

    tree = ttk.Treeview(
        history_window,
        columns=("ID", "File", "Old", "New", "Date"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("File", text="File Name")
    tree.heading("Old", text="Old Location")
    tree.heading("New", text="New Location")
    tree.heading("Date", text="Date")

    tree.column("ID", width=50)
    tree.column("File", width=180)
    tree.column("Old", width=220)
    tree.column("New", width=220)
    tree.column("Date", width=180)

    data = get_history()

    for row in data:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)


# -----------------------------
# Clear History
# -----------------------------
def delete_history():
    answer = messagebox.askyesno(
        "Confirm",
        "Do you want to delete all history?"
    )

    if answer:
        clear_history()
        messagebox.showinfo(
            "Success",
            "History deleted successfully!"
        )
def undo_last():
    record = get_last_record()

    if record is None:
        messagebox.showinfo(
            "Undo",
            "No history found."
        )
        return

    _, file_name, old_path, new_path = record

    source = os.path.join(new_path, file_name)
    destination = os.path.join(old_path, file_name)

    if os.path.exists(source):
        shutil.move(source, destination)

        messagebox.showinfo(
            "Success",
            "Last file restored successfully!"
        )
    else:
        messagebox.showerror(
            "Error",
            "File not found."
        )

# -----------------------------
# Export History
# -----------------------------
def export_history():
    data = get_history()

    with open("history.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "File Name",
            "Old Path",
            "New Path",
            "Date"
        ])

        writer.writerows(data)

    messagebox.showinfo(
        "Success",
        "History exported successfully!"
    )


# -----------------------------
# Search History
# -----------------------------
def search_history():
    keyword = search_entry.get().strip().lower()

    history_window = tk.Toplevel(root)
    history_window.title("Search Results")
    history_window.geometry("900x400")

    tree = ttk.Treeview(
        history_window,
        columns=("ID", "File", "Old", "New", "Date"),
        show="headings"
    )

    columns = {
        "ID": 50,
        "File": 180,
        "Old": 220,
        "New": 220,
        "Date": 180
    }

    for col, width in columns.items():
        tree.heading(col, text=col)
        tree.column(col, width=width)

    data = get_history()

    found = False

    for row in data:
        if keyword == "" or keyword in row[1].lower():
            tree.insert("", tk.END, values=row)
            found = True

    if not found:
        messagebox.showinfo("Search", "No matching records found.")

    tree.pack(fill="both", expand=True)
def show_statistics():
    folder = folder_path.get()

    if folder == "":
        messagebox.showerror("Error", "Please select a folder.")
        return

    total = 0

    folders = [
        "Images",
        "Documents",
        "Videos",
        "Audio",
        "Others"
    ]

    result = ""

    for f in folders:
        path = os.path.join(folder, f)

        if os.path.exists(path):
            count = len(os.listdir(path))
        else:
            count = 0

        total += count
        result += f"{f} : {count}\n"

    result = f"Total Files : {total}\n\n" + result

    messagebox.showinfo(
        "Statistics",
        result
    )

# =============================
# Main Window
# =============================
root = tk.Tk()
root.title("Smart File Organizer")
root.geometry("700x600")
root.configure(bg="#F0F8FF")
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Browse Folder", command=browse_folder)
file_menu.add_command(label="Organize Files", command=organize)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(
    label="About",
    command=lambda: messagebox.showinfo(
        "About",
        "Smart File Organizer\nVersion 1.0\nDeveloped by Prashanth"
    )
)

menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

folder_path = tk.StringVar()

status_text = tk.StringVar()
status_text.set("Ready")

title = tk.Label(
    root,
    text="📁 Smart File Organizer",
    font=("Arial", 22, "bold"),
    bg="#F0F8FF",
    fg="navy"
)
title.pack(pady=20)

entry = tk.Entry(root, textvariable=folder_path, width=50)
entry.pack(pady=10)



progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=350,
    mode="determinate"
)
progress.pack(pady=10)

browse_btn = tk.Button(
    root,
    text="📂 Browse Folder",
    command=browse_folder,
    width=25,
    height=2
)
browse_btn.pack(pady=5)

organize_btn = tk.Button(
    root,
    text="📁 Organize Files",
    command=organize,
    width=25,
    height=2
)
organize_btn.pack(pady=5)

history_btn = tk.Button(
    root,
    text="📜 View History",
    command=show_history,
    width=25,
    height=2
)
history_btn.pack(pady=5)

clear_btn = tk.Button(
    root,
    text="🗑️ Clear History",
    command=delete_history,
    width=25,
    height=2
)
clear_btn.pack(pady=5)

export_btn = tk.Button(
    root,
    text="📄 Export History",
    command=export_history,
    width=25,
    height=2,
    bg="#9C27B0",
    fg="white"
)
export_btn.pack(pady=5)
stats_btn = tk.Button(
    root,
    text="📊 Statistics",
    command=show_statistics,
    width=25,
    height=2,
    bg="#FF9800",
    fg="white"
)

stats_btn.pack(pady=5)

search_btn = tk.Button(
    root,
    text="🔍 Search History",
    command=search_history,
    width=25,
    height=2,
    bg="#009688",
    fg="white"
)
search_btn.pack(pady=5)
undo_btn = tk.Button(
    root,
    text="↩️ Undo Last Move",
    command=undo_last,
    width=25,
    height=2,
    bg="#607D8B",
    fg="white"
)

undo_btn.pack(pady=5)

status_label = tk.Label(
    root,
    textvariable=status_text,
    relief="sunken",
    anchor="w"
)
status_label.pack(fill="x", side="bottom")

root.mainloop()