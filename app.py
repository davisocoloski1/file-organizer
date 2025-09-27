import os, shutil, pyperclip
import time, threading
from tkinter import messagebox, filedialog, END

class App:
    def copy_path(self, path):
        pyperclip.copy(path)

    def check_dir_exists(self, dir):
        if os.path.exists(dir):
            return True
        else:
            os.makedirs(dir, exist_ok=True)
            return True

    def organize_files(self, origin, destiny, root, progress):
        no_permission_files = []
        try:
            directory = os.path.expanduser(origin)
            destinies = ["documents", "data_files", "images", "audios", "videos", "compressed_files", "executable", "others"]
            file_types = [[".pdf", ".docx", ".doc", ".odt", ".txt", ".rtf"],
                          [".csv", ".xls", ".xlsx", ".ods", ".tsv", ".json", ".xml"],
                          [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".bmp"],
                          [".mp3", ".wav", ".aac", ".ogg", ".flac"],
                          [".mp4", ".mkv", ".avi", ".mov"],
                          [".zip", ".rar", ".7z", ".tar", ".gz"],
                          [".exe"],
                          [".msi", ".apk", ".iso"]]

            files = os.listdir(directory)
            total = len(files)

            if len(destiny.strip()) == 0:
                messagebox.showwarning("Invalid destination.", "Your destination directory is empty.")
                return

            for i, file in enumerate(files, start=1):
                path = os.path.join(directory, file)

                for destiny_name, extensions in zip(destinies, file_types):
                    if file.endswith(tuple(extensions)):
                        final = os.path.join(destiny, destiny_name)
                        if self.check_dir_exists(final):
                            try:
                                shutil.copy2(path, final)
                            except PermissionError:
                                no_permission_files.append(path)
                        break

                progress["value"] = (i / total) * 100
                root.update_idletasks()

        except FileNotFoundError:
            messagebox.showwarning("FileNotFoundError", "Directory not found.")
            return

        error_files = "\n".join(no_permission_files)
        messagebox.showwarning("PermissionError", f"No permission to copy the following files: {error_files}")
        time.sleep(3)
        progress["value"] = 0

    def open_file_dialog(self, input_dir=None, label=None):
        if input_dir is None:
            folder = filedialog.askdirectory(title="Select the destiny folder")
            label["state"] = "normal"
            label.delete(0, END)
            label.insert(0, folder)
            label["state"] = "disabled"

        else:
            folder = filedialog.askdirectory(title="Select the origin folder")
            input_dir.delete(0, END)
            input_dir.insert(0, folder)

    def start_organize(self, origin, destiny):
        t = threading.Thread(target=self.organize_files, args=(origin, destiny))
        t.start()
