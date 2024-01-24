import tkinter as tk
from tkinter import filedialog
import os
import shutil

def select_installation_directory():
    installation_directory = filedialog.askdirectory(title="Select Installation Directory")
    installation_directory_entry.delete(0, tk.END)
    installation_directory_entry.insert(0, installation_directory)

def install_application():
    source_directory = os.path.dirname(os.path.realpath(__file__))  # Uygulamanın bulunduğu dizin
    target_directory = installation_directory_entry.get()  # Kullanıcının seçtiği hedef dizin

    try:
        shutil.copytree(source_directory, os.path.join(target_directory, "ChatApp"))
        print("Installation successful!")
    except Exception as e:
        print(f"Installation failed: {e}")

# Launcher GUI
launcher_window = tk.Tk()
launcher_window.title("Chat App Installer")

# Installation directory seçimi için Entry ve Button
installation_directory_label = tk.Label(launcher_window, text="Select Installation Directory:")
installation_directory_label.pack(pady=10)

installation_directory_entry = tk.Entry(launcher_window, width=40)
installation_directory_entry.pack(pady=10)

browse_button = tk.Button(launcher_window, text="Browse", command=select_installation_directory)
browse_button.pack(pady=10)

# Install Button
install_button = tk.Button(launcher_window, text="Install", command=install_application)
install_button.pack(pady=20)

# Launcher'ı başlat
launcher_window.mainloop()
