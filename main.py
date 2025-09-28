from platform import win32_edition
from time import sleep
from tkinter import Button, Label, Entry, Tk, Frame, Checkbutton, IntVar
from tkinter.ttk import Progressbar
from app import App

app = App()

root = Tk()
root.title("File Organizer")
root.update_idletasks()
root.minsize(width=300, height=150)
root.protocol("WM_DELETE_WINDOW", root.destroy)

var1 = IntVar()
var2 = IntVar()

content = Frame(root, bd=10)
content.grid(column=0, row=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Labels
label = Label(content, text="File Organizer", font=("Arial", 12), anchor="center")
label.grid(column=1, row=0, columnspan=3, sticky="we", pady=5)

label2 = Label(content, text="Origin Directory: ", font=("Arial", 12))
label2.grid(column=0, row=1)

label3 = Label(content, text="Destination: ", font=("Arial", 12))
label3.grid(column=0, row=3)

origin_dir_error_label = Label(content, text="", fg="red")
origin_dir_error_label.grid(column=1, row=2)
origin_dir_error_label.grid_remove()

destiny_dir_error_label = Label(content, text="", fg="red")
destiny_dir_error_label.grid(column=1, row=4)
destiny_dir_error_label.grid_remove()

nothing_to_copy_error = Label(content, text="", fg="red")
nothing_to_copy_error.grid(column=1, row=6)
nothing_to_copy_error.grid_remove()

# Progress Bar
progress_bar = Progressbar(content, length=100, mode="determinate")
progress_bar.grid(column=1, row=8, columnspan=2, sticky="we", pady=5)

# Inputs

input_dir = Entry(content, bd=2, width=20, font=("Arial", 12))
input_dir.grid(column=1, row=1, sticky="w")
input_dir.focus_set()

moving_to_label = Entry(content, bd=2, width=20, font=("Arial", 12), state="disabled", cursor="arrow")
moving_to_label.grid(column=1, row=3, sticky="we", pady=5)

# Buttons
search_origin_dir_btn = Button(content, text="Search", command=lambda: app.open_file_dialog(input_dir))
search_origin_dir_btn.grid(column=2, row=1, padx=5, sticky="we")

move_to_dir_btn = Button(content, text="Move to", command=lambda: app.open_file_dialog(label=moving_to_label))
move_to_dir_btn.grid(column=2, row=3, pady=5, padx=5, sticky="we")

organize_button = Button(content, text="Organize Files", command=lambda: app.organize_files(input_dir.get(), moving_to_label.get(), root, progress_bar, var1, var2, origin_error=origin_dir_error_label, destiny_error=destiny_dir_error_label))
organize_button.grid(column=1, row=7, columnspan=2, pady=5, sticky="we")

copy_path_button = Button(content, text="Copy Path", width=20, command=lambda: app.copy_path(moving_to_label.get(), nothing_to_copy_error))
copy_path_button.grid(column=2, row=5, padx=5, sticky="nswe")

# Checkboxes

check_existing_files = Checkbutton(content, text="Check for\nexisting\nirectories", variable=var2)
check_existing_files.grid(column=1, row=5, sticky="e")

ignore_checkbox = Checkbutton(content, text="Auto ignore\nexisting\ndirectories", variable=var1)
ignore_checkbox.grid(column=1, row=5, sticky="w")

if __name__ == '__main__':
    root.mainloop()
