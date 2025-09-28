import os, shutil, pyperclip
import time, threading
from tkinter import messagebox, filedialog, END, IntVar

class App:
    def show_hide_error(self, label, msg, type):
        if type == "show":
            if label:
                label["text"] = msg
                label.grid()

        elif type == "hide":
            if label:
                label["text"] = ""
                label.grid_remove()

    def copy_path(self, path, error_label):
        if len(path) == 0:
            error_label["text"] = "Nothing to copy"
            error_label.grid()
        else:
            pyperclip.copy(path)
            error_label["text"] = ""
            error_label.grid_remove()

    def check_dir_exists(self, dir):
        if os.path.exists(dir):
            override = messagebox.askyesnocancel("Override files", f"Path {dir} already exists, do you want to override it?")
            if override:
                return True
            if override is False:
                return False
            else:
                return None
        else:
            os.makedirs(dir, exist_ok=True)
            return True

    def checkboxes_state(self, var1, var2, dir):
        if var1 == 1:
            return True

        if var2 == 1:
            return self.check_dir_exists(dir)

    def organize_files(self, origin, destiny, root, progress, var1, var2, **kwargs):
        self.show_hide_error(kwargs.get("origin_error"), "", "hide")
        self.show_hide_error(kwargs.get("destiny_error"), "", "hide")

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
                self.show_hide_error(kwargs.get("destiny_error"), "Diretory not found or non-existent", "show")
                return

            valid_dirs = {}
            for destiny_name in destinies:
                final = os.path.join(destiny, destiny_name)
                state = self.checkboxes_state(var1.get(), var2.get(), final)

                if state:
                    valid_dirs[destiny_name] = True
                else:
                    valid_dirs[destiny_name] = False

            for i, file in enumerate(files, start=1):
                path = os.path.join(directory, file)

                for destiny_name, extensions in zip(destinies, file_types):
                    if file.endswith(tuple(extensions)):
                        if valid_dirs.get(destiny_name):
                            try:
                                shutil.copy2(path, os.path.join(destiny, destiny_name))
                            except PermissionError:
                                no_permission_files.append(path)
                        break

                progress["value"] = (i / total) * 100
                root.update_idletasks()

        except FileNotFoundError:
            self.show_hide_error(kwargs.get("origin_error"), "Diretory not found or non-existent", "show")
            return

        error_files = "\n".join(no_permission_files)
        messagebox.showwarning("PermissionError", f"No permission to copy the following files: {error_files}")
        time.sleep(3)
        progress["value"] = 0
        messagebox.showinfo("Sucess", "Transfer succesfully completed.")

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
        t = threading.Thread(target=self.organize_files, args=(origin, destiny), daemon=True)
        t.start()
