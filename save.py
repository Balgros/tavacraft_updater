import os
import random
import requests
import threading
import zipfile
import shutil
import time
import sys
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Global variables
progress_bar = None

def convert_size_to_bytes(size_str):
    size_str = size_str.upper()
    if "K" in size_str:
        return int(size_str.replace('K', '')) * 1024
    elif "M" in size_str:
        return int(size_str.replace('M', '')) * 1024 * 1024
    elif "G" in size_str:
        return int(size_str.replace('G', '')) * 1024 * 1024 * 1024
    else:
        return int(size_str)

def get_modpack_download_link():
    url = "https://tavacraft.ch/wpdm/Mods/Full_Modpack/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    for row in reversed(rows):  # reverse to get the latest version
        cells = row.find_all('td')
        if len(cells) > 1:
            link = cells[1].find('a').get('href')
            if link.endswith('.zip'):
                file_size = cells[3].text.strip()
                return url + link, file_size

    return None, None

def get_local_modpack_version():
    try:
        with open(os.path.join(os.environ['APPDATA'], '.minecraft', 'tavacraft_updater.txt'), 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def create_mods_folder_if_not_exists():
    mods_folder_path = os.path.join(os.environ['APPDATA'], '.minecraft', 'mods')  # Fix: Use 'mods' folder in lowercase
    if not os.path.exists(mods_folder_path):
        os.makedirs(mods_folder_path)

def delete_mods_content_only():
    mods_folder_path = os.path.join(os.environ['APPDATA'], '.minecraft', 'mods')  # Fix: Use 'mods' folder in lowercase
    for file_name in os.listdir(mods_folder_path):
        file_path = os.path.join(mods_folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Beim Versuch, Dateien im 'mods'-Ordner zu löschen, trat ein Fehler auf: {e}")

def show_popup(message):
    messagebox.showinfo('Info', message)

def update_status_text(label):
    tool_texts = [
        "Schärfen der verzauberten Schwämme...",
        "Optimiere den Wachstumszyklus der Mooshroom-Kühe...",
        "Überprüfe die Kompatibilität von Feuerwerksraketen mit Enderperlen...",
        "Entwickle eine Brücke aus TNT zwischen Netherfestungen...",
        "Scanne den Ozean nach verlorenen Delfin-Einhörnern...",
        "Erstelle einen Schatzkarten-Generator für Unterwassertempel...",
        "Konfiguriere die Schwerkraft für schwebende Creepers...",
        "Überwache den Lachgasgehalt in Lachstränken...",
        "Baue eine Portalverbindung zwischen dem Oberwelt-Dschungel und dem Nether-Endportal...",
        "Kalibriere die Zeitmaschine, um Steve zurück in die Kreidezeit zu schicken...",
        "Programmiere den Kuh-Milchautomaten, um Diamantmilch zu produzieren",
        "Überprüfe die Luftqualität in den Enderhöhlen...",
        "Entwickle einen Tarnumhang für Creeper, der sie wie Schafe aussehen lässt...",
        "Scanne den Himmel nach fliegenden Gravitationsblöcken...",
        "Erstelle einen Trampolin-Block für wilde Kaninchen...",
        "Optimiere die Keksproduktion in Dorfbewohner-Backöfen...",
        "Baue eine Landeplattform für außerirdische Schweinezombies...",
        "Programmiere eine Steuerung für schwebende Unterwasser-TNT-Kanonen...",
        "Überprüfe die Schwerkraft in den Schwebenden Inseln...",
    ]

    random_text = random.choice(tool_texts)
    label.config(text=random_text)

def on_update_button_click():
    # move the components as specified
    update_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    threading.Thread(target=update_modpack).start()

def update_modpack():
    global status_label, progress_bar
    current_version = get_local_modpack_version()
    download_link, file_size = get_modpack_download_link()

    if download_link is not None and download_link.split('/')[-1] != current_version:
        # Lösche den Inhalt des "mods"-Ordners, um Platz für die aktualisierten Mods zu machen
        delete_mods_content_only()

        # Zeige den Ladebildschirm und starte den Fortschrittsbalken
        progress_bar.place(relx=0.5, rely=0.7, anchor=CENTER)
        update_status_text(status_label)

        # Download und Entpacken des Modpacks
        response = requests.get(download_link, stream=True)
        total_size_in_bytes = convert_size_to_bytes(file_size)
        block_size = 1024

        progress_bar['maximum'] = total_size_in_bytes
        progress_bar['value'] = 0

        file_name = download_link.split("/")[-1]
        target_path = os.path.join(os.environ['APPDATA'])

        with open(os.path.join(target_path, file_name), 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar['value'] += len(data)
                root.update_idletasks()

        with zipfile.ZipFile(os.path.join(target_path, file_name), 'r') as zip_ref:
            create_mods_folder_if_not_exists()
            zip_ref.extractall(os.path.join(os.environ['APPDATA'], '.minecraft'))
            zip_ref.close()

        os.remove(os.path.join(target_path, file_name))

        # Speichere die aktualisierte Version in der "tavacraft_updater.txt"-Datei
        with open(os.path.join(os.environ['APPDATA'], '.minecraft', 'tavacraft_updater.txt'), 'w') as file:
            file.write(file_name)

        print(f"Modpack wurde erfolgreich aktualisiert auf Version {file_name}.")
        show_popup(f"Modpack wurde erfolgreich aktualisiert auf Version {file_name}.")

        root.quit()  # Schließe die Anwendung nach dem Update

    else:
        show_popup('Das Modpack ist bereits auf dem neuesten Stand.')
        update_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Verstecke den Fortschrittsbalken und den Status-Label
    root.after(0, progress_bar.place_forget)
    root.after(0, status_label.place_forget)

if __name__ == "__main__":
    root = Tk()
    root.title("TavaCraft Updater")
    root.geometry("600x420")

    icon_path = os.path.join('Bild', 'icon.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    image_path = os.path.join('Bild', 'background.png')
    if os.path.exists(image_path):
        background_image = Image.open(image_path)
        background_image = background_image.resize((600, 420), Image.LANCZOS)
        photo_img = ImageTk.PhotoImage(background_image)
        background_label = Label(root, image=photo_img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    status_label = Label(root, text="", bg='#A5A5A5', fg='black', font=('Arial', 12))
    status_label.place(relx=0.5, rely=0.6, anchor=CENTER)

    update_button = Button(root, text="Update Modpack", command=on_update_button_click, bg='green', fg='white', font=('Arial', 14))
    update_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('blue.Horizontal.TProgressbar', background='#1364B5', thickness=25)  # Änderung der Höhe des Ladebalkens

    progress_bar = ttk.Progressbar(root, length=int(600*0.8), mode='determinate', value=0, maximum=100, style='blue.Horizontal.TProgressbar')
    progress_bar.place_forget()

    root.mainloop()
