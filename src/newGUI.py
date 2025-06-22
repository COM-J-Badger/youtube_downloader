import tkinter as tk

root = tk.Tk()
root.title("YouTube Audio Converter & Downloader")

window_width = 300
window_height = 200

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


message = tk.Label(root, text="This is a message")
message.pack()

# keep the window displaying
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()