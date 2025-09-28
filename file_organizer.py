import os, shutil, pyperclip
import time, threading
from tkinter import messagebox, filedialog, END, IntVar, Checkbutton


class FileOrganizer:
    def __init__(self, root):
        self.vars_list = []
        self.select_all_var = IntVar(master=root)

    def show_hide_error(self, label, msg, type, color="red"):
        if type == "show":
            if label:
                label["text"] = msg
                label["fg"] = color
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

    def checkbox_state(self, vars_list):
        states = []
        for i, var in enumerate(vars_list):
            states.append(var.get())
        return states

    def toggle_checkboxes(self):
        state = self.select_all_var.get()
        for var in self.vars_list:
            var.set(state)

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

    def scan_files(self, **kwargs):
        origin = kwargs.get("origin", "")
        file_extensions = kwargs.get("file_extensions", "")
        destinies = kwargs.get("destinies", "")
        load_bar = kwargs.get("load_bar", "")
        root = kwargs.get("root")
        frame = kwargs.get("frame")
        error_label = kwargs.get("error_label")

        existing_extensions = [[] for _ in destinies]

        for widget in frame.winfo_children():
            widget.destroy()

        try:
            directory = os.path.expanduser(origin)
            files = os.listdir(directory)
            total = len(files)


            for idx, file in enumerate(files):
                _, ext = os.path.splitext(file)

                for i, extensions in enumerate(file_extensions):
                    if ext in extensions:
                        if ext not in existing_extensions[i]:
                            existing_extensions[i].append(ext)
                        break

                load_bar["value"] = (idx / total) * 100
                root.update_idletasks()

            self.show_hide_error(error_label, "Scan Complete", "show", color="green")
            time.sleep(2)
            load_bar["value"] = 0
            frame.grid()

            self.vars_list = []
            for i, _ in enumerate(destinies):
                var = IntVar(value=0)
                if existing_extensions[i]:
                    Checkbutton(frame, text=destinies[i], variable=var).grid(column=i // 2, row=i % 2, sticky="w")
                self.vars_list.append(var)

            select_all_checkbox = Checkbutton(frame, text="Select All", variable=self.select_all_var, command=lambda : self.toggle_checkboxes())
            select_all_checkbox.grid(column=0, row=len(self.vars_list)+1, columnspan=4, sticky="we")

        except FileNotFoundError:
            self.show_hide_error(error_label, "Diretory not found or non-existent", "show")
            frame.grid_remove()
            for widget in frame.winfo_children():
                widget.destroy()

    def organize_files(self, origin, destiny, root, progress, var1, **kwargs):
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
            for i, destiny_name in enumerate(destinies):
                final = os.path.join(destiny, destiny_name)
                try:
                    if self.vars_list[i].get() == 1:
                        if var1.get() == 1:
                            os.makedirs(final, exist_ok=True)
                            state = True
                        else:
                            state = self.check_dir_exists(final)
                        valid_dirs[destiny_name] = True
                    else:
                        valid_dirs[destiny_name] = False

                except IndexError:
                    if var1.get() == 1:
                        os.makedirs(final, exist_ok=True)
                        state = True
                    else:
                        state = self.check_dir_exists(final)

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

        except PermissionError:
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
