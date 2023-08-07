import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time

# Versionsnummer des Updater-Tools
updater_version = "1.0"

def fill_progress_bar(progress_canvas, percentage):
    progress_canvas.itemconfig("bar", width=percentage)

def download_modpack(download_link, save_path, progress_canvas, update_button, status_label):
    filename = os.path.join(save_path, download_link.split('/')[-1])
    download_thread = threading.Thread(target=download_file, args=(download_link, filename, progress_canvas, update_button, status_label))
    download_thread.start()

def download_file(download_link, filename, progress_canvas, update_button, status_label):
    response = requests.get(download_link, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kbyte
        num_iters = total_size // block_size
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(block_size):
                f.write(chunk)
                fill_progress_bar(progress_canvas, 100 * (f.tell() / total_size))
                update_status_text(status_label)
    else:
        messagebox.showerror("Fehler", "Fehler beim Herunterladen des Modpacks.")
    update_button.pack()
    status_label.pack(pady=20)

def get_modpack_download_link():
    url = "https://tavacraft.ch/wpdm/Mods/Full_Modpack/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        download_link = None
        download_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]
        download_links.sort(reverse=True)
        if download_links:
            download_link = url + download_links[0]
        return download_link
    else:
        messagebox.showerror("Fehler", "Fehler beim Verbinden zur Website.")
        return None

def on_update_button_click():
    update_button.pack_forget()
    progress_canvas.pack(pady=20)
    status_label.config(text="Suche nach dem Chaos in Minecraft...")
    status_label.pack(pady=20, anchor="w", padx=10)
    download_link = get_modpack_download_link()
    if download_link:
        save_path = filedialog.askdirectory(title="Speicherpfad wählen")
        if save_path:
            download_modpack(download_link, save_path, progress_canvas, update_button, status_label)

root = tk.Tk()
root.title("TavaCraft - Modpack Updater")
root.geometry("500x400")
logo_path = "N:/myCloud/03_Hobbies/05_Programmieren Lernen/MInecraft Updater/Bild/Logo_Updater.png"
logo_image = tk.PhotoImage(file=logo_path)
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(pady=20)
version_label = tk.Label(root, text=f"Updater Version {updater_version}", font=("Helvetica", 12), fg="#81C784")
version_label.pack(pady=20, anchor="center")
update_button = tk.Button(root, text="Update", bg="#81C784", fg="white", font=("Helvetica", 20, "bold"), command=on_update_button_click)
update_button.pack(pady=20)
progress_canvas = tk.Canvas(root, width=400, height=20, bg="white", bd=0, highlightthickness=0)
progress_bar = progress_canvas.create_rectangle(0, 0, 1, 20, fill="#1364B5", width=0)
progress_canvas.pack_forget()
status_label = tk.Label(root, text="", font=("Helvetica", 12), wraplength=450, justify="left")
status_label.pack_forget()
root.mainloop()
