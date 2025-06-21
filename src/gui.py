# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from backend import download_video
import threading

class YouTubeDownloaderUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("700x400")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")

        self.create_widgets()

    def create_widgets(self):
        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Output Folder:").pack(anchor="w")
        self.output_path_var = tk.StringVar()
        tk.Label(frame, textvariable=self.output_path_var, relief="sunken", width=30).pack(fill="x", pady=(0, 10))
        tk.Button(frame, text="Browse...", command=self.select_output_folder).pack(fill="x")

        tk.Label(frame, text="Download Format:").pack(anchor="w", pady=(20, 0))
        self.mp3_var = tk.BooleanVar(value=True)
        self.mp4_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="MP3", variable=self.mp3_var).pack(anchor="w")
        tk.Checkbutton(frame, text="MP4", variable=self.mp4_var).pack(anchor="w")

        button_frame = tk.Frame(frame)
        button_frame.pack(fill="x", pady=(20, 0))
        tk.Button(button_frame, text="Start", command=self.start_download).pack(side="left", expand=True, fill="x", padx=(0, 5))
        tk.Button(button_frame, text="Cancel", command=self.cancel_download).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def create_right_panel(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(frame, text="Video URLs:").pack(anchor="w")
        list_frame = tk.Frame(frame)
        list_frame.pack(fill="both", expand=True)

        self.urls_listbox = tk.Listbox(list_frame)
        self.urls_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.urls_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.urls_listbox.config(yscrollcommand=scrollbar.set)

        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill="x", pady=(10, 0))
        self.url_entry = tk.Entry(entry_frame)
        self.url_entry.pack(side="left", fill="x", expand=True)
        tk.Button(entry_frame, text="Add", command=self.add_url).pack(side="left", padx=(5, 0))

    def select_output_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path_var.set(path)

    def add_url(self):
        url = self.url_entry.get().strip()
        if url:
            self.urls_listbox.insert(tk.END, url)
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid URL.")

    

    def start_download(self):
        selected_format_mp3 = self.mp3_var.get()
        selected_format_mp4 = self.mp4_var.get()
        output_path = self.output_path_var.get()

        if not output_path:
            messagebox.showwarning("Output Folder", "Please select an output folder.")
            return

        if not (selected_format_mp3 or selected_format_mp4):
            messagebox.showwarning("Format", "Please select at least one download format (MP3 or MP4).")
            return

        # Run in a background thread
        threading.Thread(target=self._process_download_queue, args=(selected_format_mp3, selected_format_mp4, output_path), daemon=True).start()

    def _process_download_queue(self, as_mp3, as_mp4, output_path):
        total = self.urls_listbox.size()
        index = 0

        error_urls = []

        while self.urls_listbox.size() > 0:
            url = self.urls_listbox.get(0)

            try:
                download_video(
                    url=url,
                    output_path=output_path,
                    #as_mp3=as_mp3,
                    #as_mp4=as_mp4,
                    #progress_hook=self.print_progress
                )
            except Exception as e:
                #messagebox.showerror("Download Error", f"Error downloading:\n{url}\n\n{str(e)}")
                error_urls.append(url)
            finally:
                # Remove from Listbox after processing
                self.urls_listbox.delete(0)

        messagebox.showinfo(f"Download Complete", f"{total} URLs processed.\n"
        f"Errors: {len(error_urls)}" if error_urls else "All downloads completed successfully.")

        if error_urls:
            f = open(f"{output_path}/errors.txt", "a")
            for url in error_urls:
                f.write(f"{url}\n")
                f.close()
            messagebox.showinfo("Errors", f"Error URLs saved to {output_path}/errors.txt")


    def cancel_download(self):
        # Placeholder for cancellation logic
        messagebox.showinfo("Cancel", "Download cancelled.")

    def print_progress(self, d):
        #print(d)  # You can update this to a real progress bar later
        print(f"Progress: {d.get('downloaded_bytes', 0)} bytes downloaded.")

