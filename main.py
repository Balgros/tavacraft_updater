import os
import random
import requests
import threading
import zipfile
import shutil
import time
import sys
import subprocess
import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

# Global variables
progress_bar = None

def get_minecraft_folder_path():
    """Gibt den Pfad zum .minecraft-Ordner zurück, abhängig vom Betriebssystem."""
    if sys.platform.startswith('win'):
        return os.path.join(os.environ['APPDATA'], '.minecraft')
    elif sys.platform == 'darwin':  # macOS
        return os.path.expanduser('~/Library/Application Support/minecraft')
    else:
        raise OSError("Dieses Betriebssystem wird nicht unterstützt.")

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
    minecraft_folder = get_minecraft_folder_path()
    
    try:
        with open(os.path.join(minecraft_folder, 'tavacraft_updater.txt'), 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
    
def create_mods_folder_if_not_exists():
    minecraft_folder = get_minecraft_folder_path()
    mods_folder_path = os.path.join(minecraft_folder, 'mods')  # Verwenden Sie den 'mods'-Ordner in Kleinbuchstaben
    if not os.path.exists(mods_folder_path):
        os.makedirs(mods_folder_path)

def delete_mods_content_only():
    minecraft_folder = get_minecraft_folder_path()
    mods_folder_path = os.path.join(minecraft_folder, 'mods')  # Verwenden Sie den 'mods'-Ordner in Kleinbuchstaben
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
    
#Forge Check
def get_forge_download_link():
    url = "https://tavacraft.ch/wpdm/Mods/ForgeVersion/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    for row in reversed(rows):  # reverse to get the latest version
        cells = row.find_all('td')
        if len(cells) > 1:
            link = cells[1].find('a').get('href')
            if link.endswith('.jar'):
                file_size = cells[3].text.strip()
                return url + link, file_size
    return None, None

def on_forge_update_button_click():
    on_forge_update()
    
def on_forge_update():
    download_link, file_size = get_forge_download_link()
    if not download_link:
        messagebox.showerror('Fehler', 'Konnte die Forge-Version nicht abrufen.')
        return

    # Extrahieren Sie den Dateinamen aus dem Download-Link
    file_name = download_link.split("/")[-1]

    # Lassen Sie den Benutzer den Speicherort auswählen und setzen Sie den Dateinamen als Vorschlag
    target_path = filedialog.asksaveasfilename(initialfile=file_name, defaultextension=".jar", filetypes=[("Java Archive", "*.jar")])

    if not target_path:
        return  # Der Benutzer hat abgebrochen

    # Zeige den Ladebildschirm und starte den Fortschrittsbalken
    response = requests.get(download_link, stream=True)
    block_size = 1024  # 1 KB
    total_size = int(response.headers.get('content-length', 0))
    progress_bar['maximum'] = total_size

    with open(target_path, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)
            progress_bar['value'] += len(data)
            root.update_idletasks()

    # Informieren Sie den Benutzer, dass der Download abgeschlossen ist und wo er die Datei finden kann
    messagebox.showinfo("Download abgeschlossen", f"Download abgeschlossen. Datei gespeichert unter: {target_path}\nBitte führen Sie die .jar-Datei aus.")

    
#Modpack Update 

def on_update_button_click():
    # move the components as specified
    update_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    update_button.place_forget()
    threading.Thread(target=update_modpack).start()
    

def update_modpack():
    global status_label, progress_bar
    minecraft_folder = get_minecraft_folder_path()
    current_version = get_local_modpack_version()
    download_link, file_size = get_modpack_download_link()

    if download_link is not None and download_link.split('/')[-1] != current_version:
        delete_mods_content_only()
        progress_bar.place(relx=0.5, rely=0.7, anchor=CENTER)
        update_status_text(status_label)

        response = requests.get(download_link, stream=True)
        total_size_in_bytes = convert_size_to_bytes(file_size)
        block_size = 1024
        progress_bar['maximum'] = total_size_in_bytes
        progress_bar['value'] = 0
        file_name = download_link.split("/")[-1]
        target_path = os.path.join(minecraft_folder, 'mods', file_name)

        with open(target_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar['value'] += len(data)
                root.update_idletasks()

        with zipfile.ZipFile(target_path, 'r') as zip_ref:
            create_mods_folder_if_not_exists()
            zip_ref.extractall(os.path.join(minecraft_folder))

        os.remove(target_path)
        
        with open(os.path.join(minecraft_folder, 'tavacraft_updater.txt'), 'w') as file:
            file.write(file_name)

        progress_bar.place_forget()
        show_popup("Update erfolgreich! Das Modpack wurde aktualisiert.")
        root.quit()
    else:
        show_popup("Sie haben bereits die neueste Version des Modpacks.")
        root.quit()

    # Verstecke den Fortschrittsbalken und den Status-Label
    root.after(0, progress_bar.place_forget)
    root.after(0, status_label.place_forget)
    
#GRAPHICAL USER INTERFACE

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))

    root = Tk()
    root.title("TavaCraft Updater")
    root.geometry("600x420")

    icon_path = os.path.join(script_dir, 'Bild', 'icon.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    image_path = os.path.join(script_dir, 'Bild', 'background.png')
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
    
    # Forge Update Button
    forge_update_button = Button(root, text="Get Forge", command=on_forge_update_button_click, bg='#333333', fg='white', font=('Arial', 10))
    forge_update_button.place(x=10, y=420-10-forge_update_button.winfo_reqheight())  # Platziert den Button unten links mit 10px Abstand

    root.mainloop()
