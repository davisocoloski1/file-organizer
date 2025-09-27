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
label3.grid(column=0, row=2)

# Progress Bar
progress_bar = Progressbar(content, length=100, mode="determinate")
progress_bar.grid(column=1, row=5, columnspan=2, sticky="we", pady=5)

# Inputs
moving_to_label = Entry(content, bd=2, width=20, font=("Arial", 12), state="disabled", cursor="arrow")
moving_to_label.grid(column=1, row=2, sticky="we", pady=5)

input_dir = Entry(content, bd=2, width=20, font=("Arial", 12))
input_dir.grid(column=1, row=1, sticky="w")
input_dir.focus_set()

# Buttons
find_dir_button = Button(content, text="Search", command=lambda: app.open_file_dialog(input_dir))
find_dir_button.grid(column=2, row=1, padx=5, sticky="we")

select_new_dir = Button(content, text="Move to", command=lambda: app.open_file_dialog(label=moving_to_label))
select_new_dir.grid(column=2, row=2, pady=5, padx=5, sticky="we")

organize_button = Button(content, text="Organize Files", command=lambda: app.organize_files(input_dir.get(), moving_to_label.get(), root, progress_bar, var1, var2))
organize_button.grid(column=1, row=4, columnspan=2, pady=5, sticky="we")

copy_path_button = Button(content, text="Copy Path", width=20, command=lambda: app.copy_path(input_dir.get()))
copy_path_button.grid(column=2, row=3, padx=5, sticky="nswe")

# Checkboxes

check_existing_files = Checkbutton(content, text="Check for\nexisting\nirectories", variable=var2)
check_existing_files.grid(column=1, row=3, sticky="e")

ignore_checkbox = Checkbutton(content, text="Auto ignore\nexisting\ndirectories", variable=var1)
ignore_checkbox.grid(column=1, row=3, sticky="w")

if __name__ == '__main__':
    root.mainloop()
