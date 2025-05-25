import tkinter as tk
from tkinter import messagebox, colorchooser

def greet_user():
    name = name_entry.get()
    if name:
        greeting_label.config(text=f"Hello, {name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

def show_selected_option():
    choice = option_var.get()
    messagebox.showinfo("You Selected", f"You selected: {choice}")

def toggle_dark_mode():
    bg = "#333" if dark_mode_var.get() else "#fff"
    fg = "#fff" if dark_mode_var.get() else "#000"
    root.config(bg=bg)
    for widget in root.winfo_children():
        widget.config(bg=bg, fg=fg)

# Main Window
root = tk.Tk()
root.title("Tkinter Showcase")
root.geometry("400x450")

# Greeting section
tk.Label(root, text="Enter your name:").pack(pady=(10, 0))
name_entry = tk.Entry(root)
name_entry.pack()

tk.Button(root, text="Greet Me", command=greet_user).pack(pady=5)
greeting_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
greeting_label.pack()

# Radio Buttons
option_var = tk.StringVar(value="Option 1")
tk.Label(root, text="Choose an option:").pack(pady=(15, 0))
for option in ["Option 1", "Option 2", "Option 3"]:
    tk.Radiobutton(root, text=option, variable=option_var, value=option).pack(anchor='w')

tk.Button(root, text="Show Selected Option", command=show_selected_option).pack(pady=5)

# Checkbutton
dark_mode_var = tk.BooleanVar()
tk.Checkbutton(root, text="Enable Dark Mode", variable=dark_mode_var, command=toggle_dark_mode).pack(pady=10)

root.mainloop()
